# air_quality_app/app/schemas/weather.py

from pydantic import BaseModel, Field, root_validator
from typing import List, Dict, Optional, Any

# Basic weather condition model
class WeatherCondition(BaseModel):
    id: int
    main: str  # Group of weather parameters (Rain, Snow, Clouds etc.)
    description: str  # Weather condition within the group
    icon: str  # Weather icon id

# Main temperature/pressure/humidity data
class MainWeather(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int

    model_config = {"populate_by_name": True}

# Wind data
class Wind(BaseModel):
    speed: float
    deg: int  # Wind direction, degrees (meteorological)
    gust: Optional[float] = None

# Cloud data
class Clouds(BaseModel):
    all: int  # Cloudiness, %

# Rain volume (can be 1h or 3h)
class Rain(BaseModel):
    volume: Optional[float] = None

    @root_validator(pre=True)
    def extract_volume(cls, values):
        values["volume"] = values.get("1h") or values.get("3h")
        return values

    model_config = {"populate_by_name": True}

# Snow volume (can be 1h or 3h)
class Snow(BaseModel):
    volume: Optional[float] = None

    @root_validator(pre=True)
    def extract_volume(cls, values):
        values["volume"] = values.get("1h") or values.get("3h")
        return values

    model_config = {"populate_by_name": True}

# Current Weather Response Model
class CurrentWeatherResponse(BaseModel):
    coord: Dict[str, float]
    weather: List[WeatherCondition]
    base: str
    main: MainWeather
    visibility: Optional[int] = None
    wind: Wind
    clouds: Clouds
    rain: Optional[Rain] = None
    snow: Optional[Snow] = None
    dt: int  # Time of data calculation, Unix, UTC
    timezone: int  # Shift in seconds from UTC
    name: str  # City name
    cod: int

    model_config = {"populate_by_name": True}

# Forecast list item (for 5-day forecast)
class ForecastListItem(BaseModel):
    dt: int
    main: MainWeather
    weather: List[WeatherCondition]
    clouds: Clouds
    wind: Wind
    visibility: Optional[int] = None
    pop: float  # Probability of precipitation
    rain: Optional[Rain] = None
    snow: Optional[Snow] = None
    sys: Dict[str, str]  # e.g., {"pod": "d"} for part of day
    dt_txt: str  # Date in ISO 8601 format

    model_config = {"populate_by_name": True}

# 5-Day Forecast Response Model
class ForecastWeatherResponse(BaseModel):
    cod: str
    message: int
    cnt: int
    list: List[ForecastListItem]
    city: Dict[str, Any]  # Contains city name, coordinates, timezone, etc.

    model_config = {"populate_by_name": True}
