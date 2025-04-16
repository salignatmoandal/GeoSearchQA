from fastapi import APIRouter, Request
from app.model.ollama import OllamaClient
from app.context.location import LocationService
from app.core.prompt_builder import PromptBuilder
from typing import Dict
import time

router = APIRouter()
ollama_client = OllamaClient()

@router.post("/v1/chat/completions")
async def chat_completion(request: Request) -> Dict:
    body = await request.json()
    query = body["messages"][-1]["content"]
    
    # Récupération de la localisation
    client_ip = request.client.host
    location = await LocationService.get_location_from_ip(client_ip)
    if not location:
        location = LocationService.mock_location()
    
    # Construction du prompt avec contexte
    prompt = PromptBuilder.build_prompt(
        query=query,
        location=location,
        search_results=[]  # À implémenter avec Brave Search API
    )
    
    # Génération de la réponse
    response = await ollama_client.generate_completion(prompt)
    
    return {
        "id": "chatcmpl-" + str(hash(prompt))[:8],
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "local-llama2",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": response["response"]
            },
            "finish_reason": "stop"
        }]
    }
