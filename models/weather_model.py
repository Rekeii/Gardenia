from pydantic import BaseModel, Field
from typing import List, Optional

class WeatherData(BaseModel):
    temperature: float = Field(..., description="Temperature in Celsius")
    condition: str = Field(..., description="Weather condition (e.g., 'Clear', 'Rain', 'Clouds')")
    precipitation: float = Field(..., description="Precipitation in mm")
    city: Optional[str] = Field(None, description="City name")
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")


class WeatherForecastItem(BaseModel):
    time: str = Field(..., description="Forecast time (ISO8601 format)")  # Open-Meteo uses strings
    temperature_2m: float = Field(..., description="Temperature at 2m in Celsius")
    precipitation: float = Field(..., description="Precipitation in mm")
    weathercode: int = Field(..., description="WMO weather code")


class DailyWeatherForecast(BaseModel):
    forecast : List[WeatherForecastItem]
