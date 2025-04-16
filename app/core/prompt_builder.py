# app/core/prompt_builder.py
from app.context.location import Location
from typing import List, Dict, Optional
import json

class PromptBuilder:
    @staticmethod
    def build_prompt(query: str, location: Location, search_results: List[Dict]) -> str:
        context = f"""Location actuelle:
- Ville: {location.city}
- Pays: {location.country}
- Coordonnées: {location.latitude}, {location.longitude}

Règles importantes:
1. Si tu n'as pas d'information fiable sur un sujet, indique clairement que tu ne possèdes pas cette information.
2. Ne jamais inventer des adresses, horaires ou informations spécifiques sans source.
3. Si une question contient des termes spécifiques comme des types de vins ou de cuisines, respecte ces termes exactement.
4. Précise toujours si tes informations sont générales ou spécifiques/à jour.

"""
        
        if search_results:
            context += "Résultats de recherche pertinents:\n"
            for idx, result in enumerate(search_results, 1):
                context += f"{idx}. {result['title']} - {result['description']}\n"
        else:
            context += "Aucun résultat de recherche spécifique disponible pour cette requête.\n"

        prompt = f"""En utilisant le contexte ci-dessous, réponds à la question de manière honnête et utile.
Tu dois te concentrer sur les informations locales et pertinentes pour l'utilisateur.
Si tu n'as pas assez d'informations pour répondre précisément, indique-le clairement et suggère des alternatives.

{context}

Question: {query}

Réponse:"""
        return prompt

    @staticmethod
    def build_mcp_prompt(
        query: str, 
        location: Location, 
        search_results: List[Dict],
        include_sources: bool = False
    ) -> str:
        # Contexte de localisation
        location_context = f"""Location actuelle:
- Ville: {location.city}
- Pays: {location.country}
- Coordonnées: {location.latitude}, {location.longitude}
"""
        
        # Contexte de recherche
        search_context = ""
        if search_results:
            search_context = "Sources d'information:\n"
            for idx, result in enumerate(search_results, 1):
                search_context += f"[{idx}] {result.get('title')}\n"
                search_context += f"    URL: {result.get('url')}\n"
                search_context += f"    {result.get('description')}\n\n"
        
        # Instructions selon MCP
        instructions = """Instructions:
1. Utilise les sources fournies pour répondre à la question.
2. Si les sources ne contiennent pas l'information nécessaire, indique-le clairement.
3. Ne pas inventer des informations non présentes dans les sources.
4. Si des sources sont disponibles et pertinentes, cite-les en utilisant le format [1], [2], etc.
"""
        if include_sources:
            instructions += "5. À la fin de ta réponse, liste les sources utilisées au format [n] titre - URL\n"
        
        # Assemblage du prompt MCP
        prompt = f"""{instructions}

{location_context}

{search_context}

Question: {query}

Réponse:"""
        
        return prompt
