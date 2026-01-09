import asyncio
from ..io.schemas import MethodologyRequest, MethodologyResponse
from ..core.llm_utils import llm_chat

async def _build(concept: str, datasets, baselines, constraints) -> MethodologyResponse:
    prompt = f"""Build a step-by-step methodology for:
Concept: {concept}
Datasets: {datasets}
Baselines: {baselines}
Constraints: {constraints}

Output:
1) JSON for flowchart nodes/edges (fields: nodes:[id,label], edges:[source,target,label]).
2) Rationale text referencing similar methods in literature (no made-up citations).
"""
    content = await llm_chat(prompt, system="You design clear research methodologies with structured steps.")
    # MVP: Return content as rationale, and a minimal JSON
    flow = {"nodes":[{"id":"start","label":"Start"},{"id":"prep","label":"Data Prep"},{"id":"model","label":"Model"},{"id":"eval","label":"Evaluate"}],
            "edges":[{"source":"start","target":"prep","label":""},{"source":"prep","target":"model","label":""},{"source":"model","target":"eval","label":""}]}
    return MethodologyResponse(flowchart_json=flow, rationale=content)

def build_methodology(payload: MethodologyRequest, db, current):
    return asyncio.run(_build(payload.concept, payload.datasets, payload.baselines, payload.constraints))
