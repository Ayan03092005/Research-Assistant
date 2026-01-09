import asyncio
from ..io.schemas import TranslateRequest, TranslateResponse
from ..db import models
from ..core.llm_utils import llm_chat


def _load_doc_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return f"[Binary document at {path}. Add a PDF parser later.]"

async def _translate(text: str, target_lang: str) -> str:
    prompt = f"Translate the following into {target_lang}. Preserve structure and section headers when found:\n\n{text[:15000]}"
    return await llm_chat(prompt, system="You are a professional translator for research papers.")

def translate_paper(payload: TranslateRequest, db, current):
    doc = db.get(models.Document, payload.document_id)
    if not doc or doc.user_id != current.id:
        raise ValueError("Document not found")
    raw = _load_doc_text(doc.path)
    translated = asyncio.run(_translate(raw, payload.target_lang))
    return TranslateResponse(translated_text=translated, download_url=None)
