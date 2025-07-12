# air_quality_app/app/api/v1/endpoints/aqi.py

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.services.aqi_service import openaq_service
from app.schemas.aqi import LatestAQIResult, Location, HistoricalAQIResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get(
    "/aqi/latest",
    response_model=List[LatestAQIResult],
    summary="Get Latest AQI",
    description="Fetches the latest air quality measurements based on city or coordinates."
)
async def get_latest_aqi(
    city: Optional[str] = Query(None, description="City name (e.g., 'Delhi', 'London')"),
    latitude: Optional[float] = Query(None, description="Latitude for coordinates"),
    longitude: Optional[float] = Query(None, description="Longitude for coordinates")
):
    """
    Retrieves the most recent air quality measurements.
    Specify either a `city` or a combination of `latitude` and `longitude`.
    """
    if not city and (latitude is None or longitude is None):
        raise HTTPException(
            status_code=400,
            detail="Must provide either a 'city' or 'latitude' and 'longitude'."
        )

    coordinates_str = f"{latitude},{longitude}" if latitude is not None and longitude is not None else None

    try:
        data = await openaq_service.get_latest_aqi(city=city, coordinates=coordinates_str)
        if not data:
            raise HTTPException(status_code=404, detail="No AQI data found for the specified location.")
        return data
    except HTTPException as e:
        raise e # Re-raise FastAPI HTTP exceptions
    except Exception as e:
        logger.error(f"Error in get_latest_aqi endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching AQI data.")

@router.get(
    "/locations",
    response_model=List[Location],
    summary="Get Available Locations",
    description="Fetches a list of air quality monitoring locations available in OpenAQ."
)
async def get_available_locations(
    city: Optional[str] = Query(None, description="Filter locations by city"),
    country: Optional[str] = Query(None, description="Filter locations by country code (e.g., 'IN', 'US')"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of locations to return")
):
    """
    Retrieves a list of locations where OpenAQ has air quality data.
    Can be filtered by city or country.
    """
    try:
        data = await openaq_service.get_locations(city=city, country=country, limit=limit)
        return data
    except Exception as e:
        logger.error(f"Error in get_available_locations endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching locations.")

@router.get(
    "/aqi/historical/{location_id}",
    response_model=HistoricalAQIResponse,
    summary="Get Historical AQI Measurements",
    description="Fetches historical air quality measurements for a specific location ID."
)
async def get_historical_measurements(
    location_id: int,
    date_from: str = Query(..., description="Start date/time in ISO 8601 format (e.g., '2023-01-01T00:00:00Z')"),
    date_to: str = Query(..., description="End date/time in ISO 8601 format (e.g., '2023-01-02T00:00:00Z')"),
    limit: int = Query(1000, ge=1, le=10000, description="Maximum number of measurements to return")
):
    """
    Retrieves historical air quality measurements for a given location ID.
    Specify the time range using ISO 8601 formatted `date_from` and `date_to`.
    """
    try:
        # OpenAQ's get_measurements returns a list of individual measurements,
        # which can be wrapped in a dict to match HistoricalAQIResponse.
        measurements = await openaq_service.get_measurements(
            location_id=str(location_id), # OpenAQ expects string ID
            date_from=date_from,
            date_to=date_to,
            limit=limit
        )
        return {"measurements": measurements}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error in get_historical_measurements endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching historical AQI data.")