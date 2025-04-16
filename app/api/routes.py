from fastapi import APIRouter
from app.context.location import get_location
from app.context.favorites import get_favorites
from app.core.prompt_builder import build_prompt
from app.model.ollama import query_ollama
from fastmcp import FastMCP

router = APIRouter()
mcp = FastMCP("GeoMCP")  # Nom de ton assistant contextuel

# 👉 Optionnel : pour exposer MCP avec FastAPI
@router.post("/v1/chat/completions")
async def chat_endpoint(req: dict):
    """
    MCP-style endpoint compatible avec FastMCP
    """
    input_text = req.get("input")
    resources = req.get("resources", [])

    # Chargement du model
   
    # Chargement des ressources
    context = {}
    if "location://current" in resources:
        context["location://current"] = await get_location()
    if "favorites://list" in resources:
        context["favorites://list"] = await get_favorites()

    # Construction du prompt
    prompt = build_prompt(context.get("location://current", ""), context.get("favorites://list", []), input_text)
    # Utilisation du model  
    # Appel au modèle (Ollama)
    response = await query_ollama(prompt)

    return {
        "id": "chatcmpl-local",
        "model": "llama3",
        "choices": [
            {"message": {"role": "assistant", "content": response}}
        ]
    }
