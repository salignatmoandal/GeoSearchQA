# app/context/location.py

import httpx

async def get_location() -> str:
    """
    Récupère la localisation approximative (ville / région) par IP publique.
    Utilise le service ipapi.co
    """
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get("https://ipapi.co/json/")
            res.raise_for_status()
            data = res.json()
            city = data.get("city", "")
            region = data.get("region", "")
            return f"{city}, {region}".strip(", ")
    except Exception:
        return "Paris, Île-de-France"  # fallback par défaut
