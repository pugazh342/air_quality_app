# air_quality_app/app/api/v1/api.py

from fastapi import APIRouter
from app.api.v1.endpoints import health
from app.api.v1.endpoints import aqi
from app.api.v1.endpoints import weather # Import the new weather endpoints

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(aqi.router, tags=["Air Quality"])
api_router.include_router(weather.router, tags=["Weather"]) # Include the weather router