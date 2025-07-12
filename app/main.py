# air_quality_app/app/main.py

from fastapi import FastAPI
from app.api.api import api_router
from app.core.config import settings # Import your settings

app = FastAPI(
    title=settings.APP_NAME,
    description="API for real-time and predicted air quality data.", # You can also put this in settings
    version=settings.APP_VERSION,
    debug=settings.DEBUG # Use the debug setting
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def read_root():
    return {"message": f"Welcome to the {settings.APP_NAME}! Check /api/v1/docs for documentation."}