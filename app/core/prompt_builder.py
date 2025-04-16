# app/core/prompt_builder.py
from app.context.location import Location
from typing import List, Dict

class PromptBuilder:
    @staticmethod
    def build_prompt(query: str, location: Location, search_results: List[Dict]) -> str:
        context = f"""Location actuelle:
- Ville: {location.city}
- Pays: {location.country}
- Coordonnées: {location.latitude}, {location.longitude}

Résultats de recherche pertinents:
"""
        for idx, result in enumerate(search_results, 1):
            context += f"{idx}. {result['title']} - {result['description']}\n"

        prompt = f"""En utilisant le contexte ci-dessous, réponds à la question de manière naturelle et utile.
Tu dois te concentrer sur les informations locales et pertinentes pour l'utilisateur.

{context}

Question: {query}

Réponse:"""
        return prompt
