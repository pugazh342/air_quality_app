# air_quality_app/app/db/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base # Import Base from your database.py

# Model for Locations/Stations
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    openaq_id = Column(Integer, unique=True, index=True, nullable=True) # OpenAQ's internal location ID
    name = Column(String, index=True, nullable=False)
    city = Column(String, index=True, nullable=False)
    country = Column(String, index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    source_name = Column(String, nullable=True) # e.g., "OpenAQ", "WAQI"
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    first_detected = Column(DateTime(timezone=True), server_default=func.now())

    measurements = relationship("AQIMeasurement", back_populates="location")

    def __repr__(self):
        return f"<Location(id={self.id}, name='{self.name}', city='{self.city}')>"

# Model for AQI Measurements
class AQIMeasurement(Base):
    __tablename__ = "aqi_measurements"

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False, index=True)
    parameter = Column(String, nullable=False, index=True) # e.g., "pm25", "o3", "co"
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False) # e.g., "µg/m³"
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True) # When the measurement was taken
    source_id = Column(Integer, nullable=True) # Optional: original ID from external API if useful
    data_source = Column(String, nullable=False, default="OpenAQ") # e.g., "OpenAQ", "WeatherAPI"

    location = relationship("Location", back_populates="measurements")

    def __repr__(self):
        return f"<AQIMeasurement(id={self.id}, loc_id={self.location_id}, param='{self.parameter}', value={self.value}, ts='{self.timestamp}')>"

# Model for Weather Measurements (similar to AQI but for weather data)
class WeatherMeasurement(Base):
    __tablename__ = "weather_measurements"

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False, index=True) # Link to same locations table
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True) # When the measurement was taken
    data_source = Column(String, nullable=False, default="OpenWeatherMap")

    # Core weather parameters
    temp = Column(Float)
    feels_like = Column(Float)
    temp_min = Column(Float)
    temp_max = Column(Float)
    pressure = Column(Integer)
    humidity = Column(Integer)
    visibility = Column(Integer, nullable=True) # Optional
    wind_speed = Column(Float)
    wind_deg = Column(Integer)
    wind_gust = Column(Float, nullable=True) # Optional
    clouds_all = Column(Integer)
    weather_main = Column(String) # e.g., "Clouds", "Rain"
    weather_description = Column(String) # e.g., "overcast clouds", "light rain"
    weather_icon = Column(String)
    rain_volume = Column(Float, nullable=True) # e.g., for 1h or 3h
    snow_volume = Column(Float, nullable=True) # e.g., for 1h or 3h

    location = relationship("Location") # Simple relationship back to location

    def __repr__(self):
        return f"<WeatherMeasurement(id={self.id}, loc_id={self.location_id}, ts='{self.timestamp}', temp={self.temp})>"