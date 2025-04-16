# app/core/prompt_builder.py

def build_prompt(ctx: dict, user_question: str) -> str:
    """
    Assemble un prompt structuré avec tout le contexte enrichi.
    """
    loc = ctx.get("location", "lieu inconnu")
    favorites = ctx.get("favorites", [])
    search = ctx.get("search", [])
    memory = ctx.get("memory", "")

    fav_text = "\n".join([
        f"- {p['name']} ({p.get('note', '?')}★) : {p['desc']}"
        for p in favorites
    ]) if favorites else "Aucun lieu favori."

    search_text = "\n".join([
        f"- {s['title']}: {s['snippet']}"
        for s in search
    ]) if search else "Aucun résultat web trouvé."

    return f"""
Tu es un assistant local intelligent.
Ma localisation : {loc}

Voici mon historique récent :
{memory or 'Aucun historique.'}

Voici mes lieux préférés :
{fav_text}

Voici les résultats web actuels :
{search_text}

Ma question : \"{user_question}\"

Réponds-moi de manière utile, précise et personnalisée.
"""
