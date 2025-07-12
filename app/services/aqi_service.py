# air_quality_app/app/services/aqi_service.py

import httpx
from typing import List, Dict, Any, Optional
from app.core.config import settings
import logging

# Set up logging for this module
logger = logging.getLogger(__name__)

# OpenAQ API Base URL
OPENAQ_API_BASE_URL = "https://api.openaq.org/v2/"

class OpenAQService:
    def __init__(self):
        # OpenAQ generally does not require an API key for basic 'latest' or 'locations' queries.
        # However, if certain endpoints require it in the future, we can add it.
        # self.api_key = settings.OPENAQ_API_KEY # Keeping it in settings just in case
        pass

    async def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Helper to make an asynchronous GET request to the OpenAQ API."""
        url = f"{OPENAQ_API_BASE_URL}{endpoint}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0) # Add a timeout
                response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching from OpenAQ {endpoint}: {e.response.status_code} - {e.response.text}")
            raise # Re-raise the exception after logging
        except httpx.RequestError as e:
            logger.error(f"Network error fetching from OpenAQ {endpoint}: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while fetching from OpenAQ {endpoint}: {e}")
            raise

    async def get_latest_aqi(self, city: Optional[str] = None, coordinates: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetches the latest AQI measurements.
        You can specify either a city or coordinates.
        Coordinates should be in 'latitude,longitude' format.
        """
        params = {}
        if city:
            params["city"] = city
        elif coordinates:
            params["coordinates"] = coordinates
        else:
            logger.warning("get_latest_aqi called without city or coordinates.")
            return []

        # OpenAQ's 'latest' endpoint returns the most recent measurements for locations.
        # We might need to filter for specific pollutants or average them later.
        response_data = await self._make_request("latest", params)
        return response_data.get("results", [])

    async def get_locations(self, city: Optional[str] = None, country: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Fetches a list of locations available in OpenAQ.
        Useful for populating dropdowns or map markers.
        """
        params = {"limit": limit}
        if city:
            params["city"] = city
        if country:
            params["country"] = country

        response_data = await self._make_request("locations", params)
        return response_data.get("results", [])

    async def get_measurements(self, location_id: str, date_from: Optional[str] = None, date_to: Optional[str] = None, limit: int = 1000) -> List[Dict[str, Any]]:
        """
        Fetches historical measurements for a specific location.
        date_from and date_to should be in ISO 8601 format (e.g., 'YYYY-MM-DDTHH:MM:SSZ').
        """
        params = {"location_id": location_id, "limit": limit}
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to

        response_data = await self._make_request("measurements", params)
        return response_data.get("results", [])

# Initialize the service (can be used directly or via FastAPI's dependency injection)
openaq_service = OpenAQService()