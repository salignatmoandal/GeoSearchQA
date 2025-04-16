from fastapi import APIRouter, Request
from app.model.ollama import OllamaClient
from app.context.location import LocationService
from app.core.prompt_builder import PromptBuilder
from app.services.search_service import SearchService
from typing import Dict
import time
import logging

router = APIRouter()
ollama_client = OllamaClient()
search_service = SearchService()

@router.post("/v1/chat/completions")
async def chat_completion(request: Request) -> Dict:
    try:
        body = await request.json()
        messages = body.get("messages", [])
        
        # Extraire la dernière requête utilisateur
        user_query = next((msg["content"] for msg in reversed(messages) 
                          if msg.get("role") == "user"), "")
        
        if not user_query:
            return {"error": "No user query found in messages"}
        
        # Paramètres MCP
        mcp_params = body.get("mcp", {})
        include_sources = mcp_params.get("include_sources", False)
        max_sources = mcp_params.get("max_sources", 3)
        
        # Obtenir la localisation
        location = await LocationService.get_location_from_ip(request.client.host)
        if not location:
            location = LocationService.mock_location()
        
        # Recherche contextuelle via Brave Search API
        search_results = []
        if include_sources:
            search_results = await search_service.search_brave(
                query=user_query,
                location=location,
                count=max_sources
            )
        
        # Construction du prompt MCP
        prompt = PromptBuilder.build_mcp_prompt(
            query=user_query,
            location=location,
            search_results=search_results,
            include_sources=include_sources
        )
        
        # Génération de la réponse
        llm_response = await ollama_client.generate_completion(prompt)
        content = llm_response.get("response", "")
        
        # Préparer la réponse MCP
        response = {
            "id": f"chatcmpl-{str(hash(prompt))[:8]}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": "local-llama",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content
                },
                "finish_reason": "stop"
            }]
        }
        
        # Ajouter les sources si demandé
        if include_sources and search_results:
            response["sources"] = [{
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "snippet": result.get("description", "")
            } for result in search_results]
        
        return response
        
    except Exception as e:
        logging.error(f"Erreur: {str(e)}")
        return {
            "error": str(e),
            "choices": [{
                "message": {"role": "assistant", "content": "Erreur de traitement"},
                "finish_reason": "error"
            }]
        }
