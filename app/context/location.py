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
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"https://ipapi.co/{ip_address}/json/")
                if response.status_code == 200:
                    data = response.json()
                    # Vérifiez que toutes les clés nécessaires sont présentes
                    if all(key in data for key in ["latitude", "longitude", "city", "country_name"]):
                        return Location(
                            latitude=data["latitude"],
                            longitude=data["longitude"],
                            city=data["city"],
                            country=data["country_name"]
                        )
                    else:
                        logging.warning(f"Données de localisation incomplètes: {data}")
                else:
                    logging.warning(f"Échec de récupération de localisation: {response.status_code}")
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de localisation: {str(e)}")
        
        # En cas d'échec, utilisez la localisation par défaut
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
