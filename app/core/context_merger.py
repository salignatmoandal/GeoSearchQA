# app/core/context_merger.py

def merge_context(location: str, favorites: list, search: list, memory: str) -> dict:
    """
    Fusionne tous les blocs de contexte dans une seule structure.
    """
    return {
        "location": location,
        "favorites": favorites,
        "search": search,
        "memory": memory
    }
