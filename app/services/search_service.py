import httpx
import os
import logging
from typing import List, Dict
from app.context.location import Location

class SearchService:
    @staticmethod
    async def search_brave(
        query: str, 
        location: Location, 
        count: int = 3
    ) -> List[Dict]:
        """Recherche des informations via l'API Brave Search avec MCP"""
        try:
            api_key = os.getenv("BRAVE_API_KEY")
            if not api_key:
                logging.warning("Clé API Brave non configurée")
                return []
                
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Paramètres MCP pour Brave Search
                params = {
                    "q": query,
                    "count": count,
                    "search_lang": "fr",
                    "country": location.country.lower(),
                    "coordinate": f"{location.latitude},{location.longitude}"
                }
                
                headers = {
                    "Accept": "application/json",
                    "X-Subscription-Token": api_key
                }
                
                response = await client.get(
                    "https://api.search.brave.com/res/v1/web/search",
                    params=params,
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = []
                    
                    for item in data.get("results", []):
                        results.append({
                            "title": item.get("title", ""),
                            "description": item.get("description", ""),
                            "url": item.get("url", ""),
                            "age": item.get("age", ""),
                            "type": item.get("type", "web")
                        })
                    
                    # Ajouter des informations spécifiques à la localisation
                    if "location" in data:
                        location_data = data.get("location", {})
                        results.append({
                            "title": f"Informations locales pour {location_data.get('name', '')}",
                            "description": f"Fuseau horaire: {location_data.get('timezone', '')}, Région: {location_data.get('region', '')}",
                            "url": "",
                            "type": "location"
                        })
                    
                    return results
                else:
                    logging.error(f"Erreur Brave Search API: {response.status_code}")
                    return []
                    
        except Exception as e:
            logging.error(f"Erreur lors de la recherche Brave: {str(e)}")
            return []
