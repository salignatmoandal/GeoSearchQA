# app/context/location.py
from dataclasses import dataclass
from typing import Optional
import httpx

@dataclass
class Location:
    latitude: float
    longitude: float
    city: str
    country: str

class LocationService:
    @staticmethod
    async def get_location_from_ip(ip_address: str) -> Optional[Location]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://ipapi.co/{ip_address}/json/")
            if response.status_code == 200:
                data = response.json()
                return Location(
                    latitude=data["latitude"],
                    longitude=data["longitude"],
                    city=data["city"],
                    country=data["country_name"]
                )
        return None

    
    @staticmethod
    def mock_location() -> Location:
        return Location(
            latitude=48.8566,
            longitude=2.3522,
            city="Paris",
            country="France"
        )
