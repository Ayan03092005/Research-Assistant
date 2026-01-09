import asyncio
from typing import List, Dict, Any
from ..io.schemas import GapRequest, GapResponse, PaperBrief
from ..llm.openai_client import openai_chat
from ..core.llm_utils import llm_chat
async def _mine_gaps(aim: str, papers: List[PaperBrief]) -> GapResponse:
    refs = "\n".join([f"- {p.first_author}: {p.title} ({p.year}) {p.url or p.doi or ''}" for p in papers])
    prompt = f"""Aim: {aim}
Papers:
{refs}

Task:
1) Extract limitations/assumptions in these papers (bullet list). For each item include the source title or first author.
2) Propose aim-aligned opportunities (what to do next), each tied to at least one source.

Format:
Limitations: - limitation (with sources)
Opportunities: - idea (with rationale and sources)

"""
    content = await llm_chat(prompt, system="You are a research analyst. Be specific and cite sources by short title/author.")
    # For MVP, return the LLM text as strings inside dicts
    return GapResponse(
        limitations=[{"text": content}],
        opportunities=[{"text": "See above blocks for opportunities extracted from content.", "detail": content}]
    )

def find_research_gaps(payload: GapRequest, db, current):
    return asyncio.run(_mine_gaps(payload.aim, payload.selected_papers))
