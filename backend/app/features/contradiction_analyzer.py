import asyncio
from ..io.schemas import ContradictionRequest, ContradictionResponse
from ..core.llm_utils import llm_chat

async def _analyze(method_text: str, results_text: str, domain: str):
    prompt = f"""Methodology:\n{method_text[:8000]}\n\nResults:\n{results_text[:8000]}
Domain: {domain}
Identify conflicting claims or contradictions. For each, include:
- claim
- why contradictory
- what to check (data, setup, eval)
Return as a JSON-like bullet list (MVP text is fine).
"""
    out = await llm_chat(prompt, system="You find inconsistencies between methods and results.")
    return ContradictionResponse(conflicts=[{"text": out}])

def analyze_contradictions(payload: ContradictionRequest, db, current):
    return asyncio.run(_analyze(payload.methodology_text, payload.results_text, payload.domain))
