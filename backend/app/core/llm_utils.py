"""
app/core/llm_utils.py

Centralized LLM interface for ChatGPT (GPT-4o) and Gemini 1.5-Pro.
Only update `llm_choice` below to switch the active model globally.
No other file changes are needed.
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv
from ..config.settings import settings


# Load environment
load_dotenv()

# -------------------------------------------------------------------
# 🔧 MODEL SELECTION — change once here only
# -------------------------------------------------------------------
llm_choice = "Gemini"   # "Chatgpt" or "Gemini"
# -------------------------------------------------------------------

# API keys (from .env)
OPENAI_KEY = settings.OPENAI_API_KEY
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

# Shared HTTPX setup for OpenAI (keeps your async workflow)
OPENAI_API_BASE = "https://api.openai.com/v1"

# Gemini import (lazy)
try:
    from google import genai
    # --- FIX 1: Use the correct client initialization ---
    gemini_client = genai.Client(api_key=GEMINI_KEY)
except ImportError:
    gemini_client = None
except Exception as e:
    # Handle API key or network issues during startup
    print(f"Gemini client initialization failed: {e}")
    gemini_client = None 

# -------------------------------------------------------------------
# 🧠 Unified Async LLM Chat Function
# -------------------------------------------------------------------
async def llm_chat(
    prompt: str,
    system: str = "You are a helpful research assistant.",
    model_gpt: str = "gpt-4o",              # <-- RESTORED
    model_gemini: str = "gemini-2.5-pro" # <-- RESTORED
) -> str:

    # ---------- CASE 1: GEMINI ----------
    if llm_choice.lower() == "gemini":
        if not gemini_client:
            raise RuntimeError(
                "Gemini client failed to initialize. Check API key."
            )
            
        try:
            # --- FIX 2 & 3: Correct API call and pass System Instruction (via config) ---
            
            # The system instruction is passed via the config/system_instruction
            resp = await asyncio.to_thread(
                gemini_client.models.generate_content, # Correct method
                model=model_gemini,
                contents=prompt,
                config={
                    "system_instruction": system, # Correct way to set system role
                    "temperature": 0.2
                }
            )
            
            if resp.text:
                return resp.text.strip()
            return "[No text output from Gemini]"
        except Exception as e:
            return f"[Gemini API error: {str(e)}]"

    # ---------- CASE 2: CHATGPT (OpenAI) ----------
    
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_gpt,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post(f"{OPENAI_API_BASE}/chat/completions", headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[OpenAI API call failed: {e}]"
