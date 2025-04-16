# app/context/memory.py

import json
from pathlib import Path

MEMORY_PATH = Path("data/memory.json")

async def get_memory(limit: int = 3) -> str:
    """
    Retourne les dernières interactions utilisateur sous forme textuelle.
    """
    if not MEMORY_PATH.exists():
        return "Aucune mémoire enregistrée."

    with open(MEMORY_PATH, encoding="utf-8") as f:
        history = json.load(f)[-limit:]

    return "\n".join([f"Q: {h['question']} → R: {h['response']}" for h in history])


async def save_to_memory(question: str, response: str, location: str = ""):
    """
    Sauvegarde une interaction utilisateur dans le fichier mémoire.
    """
    MEMORY_PATH.parent.mkdir(exist_ok=True)
    history = []

    if MEMORY_PATH.exists():
        with open(MEMORY_PATH, encoding="utf-8") as f:
            history = json.load(f)

    history.append({
        "question": question,
        "location": location,
        "response": response
    })

    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history[-10:], f, indent=2)
