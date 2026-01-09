import asyncio
from ..io.schemas import PersonaSummaryRequest, PersonaSummaryResponse
from ..db import models
from ..core.llm_utils import llm_chat

def _get_text(db, payload, current) -> str:
    if payload.raw_text:
        return payload.raw_text
    if payload.document_id:
        doc = db.get(models.Document, payload.document_id)
        if not doc or doc.user_id != current.id:
            raise ValueError("Document not found")
        try:
            with open(doc.path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception:
            return "[Binary doc. Add parser later.]"
    return ""

async def _summarize(text: str, persona: str, focus: str, length: str) -> str:
    prompt = f"""Persona: {persona}
Focus: {focus}
Length: {length}

Summarize the following research content. Use clear headers and bullet points. Avoid speculation:
{text[:15000]}
"""
    return await llm_chat(prompt, system="You tailor research summaries for specific personas.")

def make_persona_summary(payload: PersonaSummaryRequest, db, current):
    text = _get_text(db, payload, current)
    out = asyncio.run(_summarize(text, payload.persona, payload.focus, payload.length))
    return PersonaSummaryResponse(summary=out)
