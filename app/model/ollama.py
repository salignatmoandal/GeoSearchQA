import httpx
from app.config import OLLAMA_HOST, MODEL_NAME

async def query_ollama(prompt: str) -> str:
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{OLLAMA_HOST}/api/generate", json=payload)
        return res.json()["response"]
