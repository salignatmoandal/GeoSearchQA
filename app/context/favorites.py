# app/context/favorites.py
# Fichier pour récupérer les lieux favoris

import json
from pathlib import Path

FAV_PATH = Path("data/favorites.json")

async def get_favorites() -> list[dict]:
    """
    Charge les lieux favoris depuis un fichier JSON local.
    """
    if not FAV_PATH.exists():
        return []
    
    with open(FAV_PATH, encoding="utf-8") as f:
        return json.load(f)
