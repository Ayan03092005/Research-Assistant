import asyncio
from ..io.schemas import CrossDomainRequest, CrossDomainResponse
from ..core.llm_utils import llm_chat

async def _synth(text: str, domains):
    prompt = f"""Draft text:\n{text[:12000]}\n\nTarget domains: {domains}
Map core constructs to each domain with concrete applications (both directions).
Return:
- mappings: list of {{domain, applications[], risks[]}}
- narrative: 2-3 paragraphs
"""
    out = await llm_chat(prompt, system="You are skilled at interdisciplinary synthesis with concrete applications.")
    return CrossDomainResponse(mappings=[{"domain": d, "applications": [], "risks": []} for d in domains], narrative=out)

def synthesize_cross_domain(payload: CrossDomainRequest, db, current):
    return asyncio.run(_synth(payload.draft_text, payload.target_domains))
