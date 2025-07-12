# air_quality_app/app/services/weather_service.py

import httpx
from typing import Dict, Any, Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# OpenWeatherMap API Base URL
OPENWEATHER_API_BASE_URL = "https://api.openweathermap.org/data/2.5/"

class OpenWeatherMapService:
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        if not self.api_key:
            logger.error("OPENWEATHER_API_KEY is not set in environment variables.")
            raise ValueError("OpenWeatherMap API Key is missing.")

    async def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Helper to make an asynchronous GET request to the OpenWeatherMap API."""
        url = f"{OPENWEATHER_API_BASE_URL}{endpoint}"
        full_params = {"appid": self.api_key, **(params or {})}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=full_params, timeout=10.0)
                response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching from OpenWeatherMap {endpoint}: {e.response.status_code} - {e.response.text}")
            raise # Re-raise the exception after logging
        except httpx.RequestError as e:
            logger.error(f"Network error fetching from OpenWeatherMap {endpoint}: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while fetching from OpenWeatherMap {endpoint}: {e}")
            raise

    async def get_current_weather(self, lat: float, lon: float, units: str = "metric") -> Dict[str, Any]:
        """
        Fetches current weather data for given coordinates.
        Units can be 'metric' (Celsius), 'imperial' (Fahrenheit), or 'standard' (Kelvin).
        """
        params = {"lat": lat, "lon": lon, "units": units}
        return await self._make_request("weather", params)

    async def get_forecast_weather(self, lat: float, lon: float, units: str = "metric", cnt: int = 40) -> Dict[str, Any]:
        """
        Fetches 5-day weather forecast data (3-hour step) for given coordinates.
        `cnt` is the number of timestamps returned (max 40 for 5 days).
        """
        params = {"lat": lat, "lon": lon, "units": units, "cnt": cnt}
        return await self._make_request("forecast", params)

# Initialize the service
openweathermap_service = OpenWeatherMapService()