# air_quality_app/app/api/v1/endpoints/weather.py

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.weather_service import openweathermap_service
from app.schemas.weather import CurrentWeatherResponse, ForecastWeatherResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get(
    "/weather/current",
    response_model=CurrentWeatherResponse,
    summary="Get Current Weather",
    description="Fetches current weather data for given coordinates."
)
async def get_current_weather_data(
    latitude: float = Query(..., description="Latitude for weather data"),
    longitude: float = Query(..., description="Longitude for weather data"),
    units: str = Query("metric", description="Units of measurement (metric, imperial, standard)")
):
    """
    Retrieves current weather conditions for specified geographical coordinates.
    """
    try:
        data = await openweathermap_service.get_current_weather(lat=latitude, lon=longitude, units=units)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error in get_current_weather_data endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching current weather data.")

@router.get(
    "/weather/forecast",
    response_model=ForecastWeatherResponse,
    summary="Get Weather Forecast",
    description="Fetches 5-day weather forecast data for given coordinates (3-hour step)."
)
async def get_forecast_weather_data(
    latitude: float = Query(..., description="Latitude for weather forecast"),
    longitude: float = Query(..., description="Longitude for weather forecast"),
    units: str = Query("metric", description="Units of measurement (metric, imperial, standard)"),
    cnt: int = Query(40, ge=1, le=40, description="Number of timestamps to return (max 40 for 5 days / 3-hour step)")
):
    """
    Retrieves a 5-day weather forecast (with data every 3 hours) for specified geographical coordinates.
    """
    try:
        data = await openweathermap_service.get_forecast_weather(lat=latitude, lon=longitude, units=units, cnt=cnt)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error in get_forecast_weather_data endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching weather forecast data.")