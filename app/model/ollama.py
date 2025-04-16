# app/model/ollama_client.py
import httpx
from app.config import Config

class OllamaClient:
    def __init__(self):
        self.base_url = Config.OLLAMA_BASE_URL
        self.model = Config.MODEL_NAME

    async def generate_completion(self, prompt: str, temperature: float = Config.DEFAULT_TEMPERATURE):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": temperature,
                }
            )
            return response.json()