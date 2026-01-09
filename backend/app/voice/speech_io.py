import httpx
import os
from fastapi import UploadFile
from ..config.settings import settings
from ..core.llm_utils import llm_chat
import google.generativeai as genai

llm = "Chatgpt"  # or "Gemini"

OPENAI_API_BASE = "https://api.openai.com/v1/audio/transcriptions"

def transcribe_audio(file: UploadFile) -> str:
    """
    Transcribes uploaded audio using either OpenAI Whisper or Gemini 1.5-Pro.
    Works with the same switch variable `llm`.
    """
    if llm.lower() == "gemini":
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))
            model = genai.GenerativeModel("gemini-1.5-pro")
            # Convert UploadFile to local temporary file for Gemini input
            tmp_path = f"/tmp/{file.filename}"
            with open(tmp_path, "wb") as tmp:
                tmp.write(file.file.read())
            # Gemini multimodal prompt
            resp = model.generate_content(["Transcribe this research-related audio:", genai.upload_file(tmp_path)])
            return resp.text.strip() if resp and resp.text else "[No output from Gemini]"
        except Exception as e:
            return f"[Gemini transcription failed: {str(e)}]"

    # ---------- Default: Whisper (OpenAI) ----------
    try:
        with httpx.Client(timeout=60.0) as client:
            files = {"file": (file.filename, file.file, file.content_type)}
            data = {"model": "whisper-1", "temperature": "0"}
            headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
            resp = client.post(OPENAI_API_BASE, headers=headers, files=files, data=data)
            resp.raise_for_status()
            result = resp.json()
            return result.get("text", "").strip()
    except Exception as e:
        return f"[Transcription failed: {str(e)}]"
