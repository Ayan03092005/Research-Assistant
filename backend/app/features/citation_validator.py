import asyncio
from ..io.schemas import CitationValidateRequest, CitationValidateResponse
from ..core.llm_utils import llm_chat

async def _validate(md: str, style: str):
    prompt = f"""Draft markdown:\n{md[:15000]}\nStyle: {style}
Tasks:
1) Highlight sentences likely requiring citations (wrap with <<CITE?>> ... >>).
2) Normalize any existing in-text citations to numeric [#] style.
3) Produce a References list skeleton at the end (placeholders OK).

Return the annotated markdown followed by a References section.
"""
    out = await llm_chat(prompt, system="You are strict about citation hygiene and styles.")
    # MVP: treat everything as a single blob; references extracted inline
    return CitationValidateResponse(annotated_markdown=out, references=[])

def validate_citations(payload: CitationValidateRequest, db, current):
    return asyncio.run(_validate(payload.draft_markdown, payload.style))
