# app/context/location.py
from dataclasses import dataclass
from typing import Optional
import httpx
import logging

@dataclass
class Location:
    latitude: float
    longitude: float
    city: str
    country: str

class LocationService:
    @staticmethod
    async def get_location_from_ip(ip_address: str) -> Optional[Location]:
        try:
            # Pour déboguer, affichons l'IP
            logging.info(f"Tentative de récupération de localisation pour IP: {ip_address}")
            
            # Les IPs privées ne fonctionneront pas avec ipapi.co
            if ip_address in ["127.0.0.1", "localhost", "::1"] or ip_address.startswith(("172.", "192.168.", "10.")):
                logging.info(f"IP privée détectée: {ip_address}. Utilisation de la localisation par défaut.")
                return LocationService.mock_location()
                
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Pour voir ce que l'API renvoie réellement
                response = await client.get(f"https://ipapi.co/{ip_address}/json/")
                logging.info(f"Statut de la réponse ipapi: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    # Afficher toutes les clés disponibles pour le débogage
                    logging.info(f"Clés disponibles dans la réponse ipapi: {list(data.keys())}")
                    logging.info(f"Réponse complète: {data}")
                    
                    # Essayer d'obtenir les valeurs avec fallback 
                    lat = data.get("latitude", 0)
                    lon = data.get("longitude", 0)
                    city = data.get("city", "Ville inconnue")
                    country = data.get("country_name", "Pays inconnu")
                    
                    return Location(
                        latitude=float(lat),
                        longitude=float(lon),
                        city=city,
                        country=country
                    )
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de localisation: {str(e)}")
        
        # En cas d'échec, utilisez toujours la localisation par défaut
        logging.info("Utilisation de la localisation par défaut")
        return LocationService.mock_location()

    @staticmethod
    def mock_location() -> Location:
        return Location(
            latitude=48.8566,
            longitude=2.3522,
            city="Paris",
            country="France"
        )
