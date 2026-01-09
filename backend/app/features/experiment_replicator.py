import asyncio
from ..io.schemas import ReplicatorRequest, ReplicatorResponse
from ..core.llm_utils import llm_chat

async def _replicate(methodology_json, candidate_papers):
    refs = "\n".join([f"- {p.first_author}: {p.title} ({p.year}) {p.url or p.doi or ''}" for p in candidate_papers])
    prompt = f"""Given this methodology JSON (nodes/edges): {methodology_json}
Papers with enhancements/new steps:
{refs}

Suggest concrete insertions/variants. Explain benefit and where they attach (node id).
Return:
- overlay_json: nodesToAdd:[...], edgesToAdd:[...], annotations:[{ '{nodeId, note}' }]
- notes: human-readable explanation
"""
    content = await llm_chat(prompt, system="You propose careful experimental enhancements grounded in cited sources.")
    overlay = {"nodesToAdd":[], "edgesToAdd":[], "annotations":[{"nodeId":"model","note":"Consider regularization from Paper [X]."}]}
    return ReplicatorResponse(overlay_json=overlay, notes=content)

def suggest_experiment_variants(payload: ReplicatorRequest, db, current):
    return asyncio.run(_replicate(payload.methodology_json, payload.candidate_papers))
