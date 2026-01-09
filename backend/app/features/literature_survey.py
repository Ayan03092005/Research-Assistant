import asyncio
from typing import List
from ..io.schemas import SurveyRequest, SurveyResponse, PaperBrief
from ..retrieval.semantic_scholar_client import search_semantic_scholar
from ..retrieval.openalex_client import search_openalex
from ..retrieval.crossref_client import search_crossref
from ..retrieval.unpaywall_client import enrich_unpaywall
from ..core.rate_limiter import JobCircuit
from ..config.constants import SOURCE_SEMANTIC_SCHOLAR, SOURCE_OPENALEX, SOURCE_CROSSREF, DEFAULT_SURVEY_RESULTS
from ..core.llm_utils import llm_chat

async def _search_all(query: str, n_results: int, year_from: int | None, year_to: int | None) -> List[PaperBrief]:
    jc = JobCircuit()
    results: List[PaperBrief] = []

    # 1) Semantic Scholar
    if not jc.is_off(SOURCE_SEMANTIC_SCHOLAR) and len(results) < n_results:
        try:
            s2 = await search_semantic_scholar(query, limit=min(n_results, 20))
            results.extend([PaperBrief(**p) for p in s2])
        except Exception:
            jc.mark_off(SOURCE_SEMANTIC_SCHOLAR)

    # 2) OpenAlex
    if not jc.is_off(SOURCE_OPENALEX) and len(results) < n_results:
        try:
            oa = await search_openalex(query, per_page=min(n_results - len(results), 20), year_from=year_from, year_to=year_to)
            results.extend([PaperBrief(**p) for p in oa])
        except Exception:
            jc.mark_off(SOURCE_OPENALEX)

    # 3) Crossref
    if not jc.is_off(SOURCE_CROSSREF) and len(results) < n_results:
        try:
            cr = await search_crossref(query, rows=min(n_results - len(results), 20))
            results.extend([PaperBrief(**p) for p in cr])
        except Exception:
            jc.mark_off(SOURCE_CROSSREF)

    # trim
    unique = []
    seen = set()
    for r in results:
        key = (r.doi or r.url or r.title)
        if key not in seen:
            seen.add(key)
            unique.append(r)
        if len(unique) >= n_results:
            break

    # OA enrichment
    enriched = []
    for r in unique:
        if r.doi:
            e = await enrich_unpaywall(r.doi) or {}
            if e.get("oa_pdf"):
                r.url = r.url or e["oa_pdf"]
        enriched.append(r)
    return enriched

def _build_citation_list(papers: List[PaperBrief]) -> str:
    lines = []
    for idx, p in enumerate(papers, 1):
        lines.append(f"[{idx}] {p.first_author} et al., “{p.title}”, {p.venue} {p.year}. {p.url or (p.doi and 'https://doi.org/'+p.doi) or ''}".strip())
    return "\n".join(lines)

async def _draft_survey(topic: str, papers: List[PaperBrief]) -> str:
    biblio = _build_citation_list(papers)
    cite_map = "\n".join([f"[{i+1}] {p.title}" for i,p in enumerate(papers)])
    prompt = f"""Topic: {topic}
You are writing a literature survey. Use only the listed papers and cite as [1], [2], etc.
Papers:
{biblio}

Write a concise literature survey (research style) with in-text numeric citations.
"""
    return await llm_chat(prompt, system="You are a rigorous academic writer. Always cite with [#].")

def generate_literature_survey(payload: SurveyRequest, db, current):
    # run async retrieval & optional draft
    async def run():
        papers = await _search_all(payload.topic + " " + " ".join(payload.keywords), payload.n_results or DEFAULT_SURVEY_RESULTS, payload.year_from, payload.year_to)
        draft = await _draft_survey(payload.topic, papers)
        return SurveyResponse(papers=papers, draft=draft)
    return asyncio.run(run())
