# air_quality_app/app/schemas/aqi.py

from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# Represents a single pollutant measurement
class Measurement(BaseModel):
    parameter: str # e.g., "pm25", "o3", "co"
    value: float
    unit: str # e.g., "µg/m³", "ppm"
    # timestamp: str # OpenAQ timestamp format can be complex, keep as str for now

# Represents a location's latest AQI data
class LatestAQIResult(BaseModel):
    location_id: Optional[int] = Field(None, alias="id") # OpenAQ uses 'id' for location, rename to location_id
    location_name: str = Field(..., alias="location")
    city: str
    country: str
    coordinates: Dict[str, float] # {"latitude": ..., "longitude": ...}
    measurements: List[Measurement]
    # lastUpdated: str # Optional field from OpenAQ response, if needed

    model_config = {'populate_by_name': True} # Allows initialization by field name or alias

# Represents an individual historical measurement entry
class HistoricalMeasurement(BaseModel):
    location_name: str = Field(..., alias="location")
    parameter: str
    value: float
    unit: str
    date_utc: str = Field(..., alias="date") # The 'date' object from OpenAQ has a 'utc' field
    coordinates: Dict[str, float]

    model_config = {'populate_by_name': True}

# Response model for fetching historical data
class HistoricalAQIResponse(BaseModel):
    measurements: List[HistoricalMeasurement]

# Simple model for a location to display on map/list
class Location(BaseModel):
    id: int
    name: str = Field(..., alias="location")
    city: str
    country: str
    latitude: float
    longitude: float

    model_config = {'populate_by_name': True}