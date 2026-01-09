import os
from ..config.settings import settings
import httpx

OPENAI_API_BASE = "https://api.openai.com/v1"

async def openai_chat(prompt: str, system: str = "You are a helpful research assistant.", model: str = "gpt-4o"):
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(f"{OPENAI_API_BASE}/chat/completions", headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]
