from fastapi import APIRouter, Request
from app.model.ollama_client import OllamaClient
from app.context.location import LocationService
from app.core.prompt_builder import PromptBuilder
from typing import Dict
import time
import logging

router = APIRouter()
ollama_client = OllamaClient()

@router.post("/v1/chat/completions")
async def chat_completion(request: Request) -> Dict:
    try:
        body = await request.json()
        query = body["messages"][-1]["content"]
        
        # Récupération de la localisation
        client_ip = request.client.host
        logging.info(f"IP client: {client_ip}")
        
        # Pour les IPs privées ou de conteneur, utilisez directement la localisation par défaut
        if client_ip in ["127.0.0.1", "localhost", "::1"] or client_ip.startswith("172.") or client_ip.startswith("192.168."):
            location = LocationService.mock_location()
            logging.info("Utilisation de la localisation mock pour IP locale")
        else:
            location = await LocationService.get_location_from_ip(client_ip)
        
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
            "model": "local-llama",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response.get("response", "Je n'ai pas pu générer une réponse.")
                },
                "finish_reason": "stop"
            }]
        }
    except Exception as e:
        logging.error(f"Erreur lors du traitement de la requête: {str(e)}")
        return {
            "error": str(e),
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Je suis désolé, une erreur s'est produite lors du traitement de votre demande."
                },
                "finish_reason": "error"
            }]
        }
