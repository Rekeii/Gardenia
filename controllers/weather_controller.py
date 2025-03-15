import httpx
from models.weather_model import WeatherData, DailyWeatherForecast , WeatherForecastItem
from typing import Optional

class WeatherController:
    def __init__(self, default_latitude: float = 14.5995, default_longitude: float = 120.9842): #Manila
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.default_latitude = default_latitude
        self.default_longitude = default_longitude

    async def get_current_weather(self, latitude: Optional[float] = None, longitude: Optional[float] = None, city: Optional[str] = None) -> WeatherData:
        latitude = latitude or self.default_latitude
        longitude = longitude or self.default_longitude

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,precipitation,weathercode",  # Request specific variables
            "timezone": "auto",  # Use the location's timezone
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

        return self._parse_current_weather_data(data, city, latitude, longitude)


    async def get_weather_forecast(self, latitude: Optional[float] = None, longitude: Optional[float] = None) -> DailyWeatherForecast:

        latitude = latitude or self.default_latitude
        longitude = longitude or self.default_longitude

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m,precipitation,weathercode",
            "timezone": "auto",
            "forecast_days": 3, #get 3 day forecast
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

        return self._parse_forecast_data(data)

    def _parse_current_weather_data(self, data: dict, city:Optional[str], latitude: float, longitude: float) -> WeatherData:
        try:
            # WMO Weather Interpretation Codes (WW) -- simplified lookup
            weather_codes = {
                0:  "Clear sky",
                1:  "Mainly clear",
                2:  "Partly cloudy",
                3:  "Overcast",
                45: "Fog",
                48: "Depositing rime fog",
                51: "Drizzle: Light",
                53: "Drizzle: Moderate",
                55: "Drizzle: Dense intensity",
                56: "Freezing Drizzle: Light",
                57: "Freezing Drizzle: Dense intensity",
                61: "Rain: Slight",
                63: "Rain: Moderate",
                65: "Rain: Heavy intensity",
                66: "Freezing Rain: Light",
                67: "Freezing Rain: Heavy intensity",
                71: "Snow fall: Slight",
                73: "Snow fall: Moderate",
                75: "Snow fall: Heavy intensity",
                77: "Snow grains",
                80: "Rain showers: Slight",
                81: "Rain showers: Moderate",
                82: "Rain showers: Violent",
                85: "Snow showers slight",
                86: "Snow showers heavy",
                95: "Thunderstorm: Slight or moderate",
                96: "Thunderstorm with slight hail",
                99: "Thunderstorm with heavy hail",
            }
             # Get condition from the weathercode
            condition = weather_codes.get(data["current"]["weathercode"], "Unknown")

            return WeatherData(
                temperature=data["current"]["temperature_2m"],
                condition=condition,
                precipitation=data["current"]["precipitation"],
                city = city,
                latitude = latitude,
                longitude = longitude,

            )
        except KeyError as e:
             raise ValueError(f"Unexpected API response structure. Missing key: {e}") from e
        except Exception as e:
            raise Exception(f"An excpetion occurred parsing weather: {e}")
    def _parse_forecast_data(self, data: dict) -> DailyWeatherForecast:
        forecast_items = []

        try:
            hourly_data = data["hourly"]
            # Loop through the time, temperature, and precipitation lists together using zip
            for time, temp, precip, code in zip(hourly_data["time"], hourly_data["temperature_2m"], hourly_data["precipitation"], hourly_data["weathercode"]):

                #For simplicity, using same weather_codes dict from previous
                weather_codes = {
                    0:  "Clear sky",
                    1:  "Mainly clear",
                    2:  "Partly cloudy",
                    3:  "Overcast",
                    45: "Fog",
                    48: "Depositing rime fog",
                    51: "Drizzle: Light",
                    53: "Drizzle: Moderate",
                    55: "Drizzle: Dense intensity",
                    56: "Freezing Drizzle: Light",
                    57: "Freezing Drizzle: Dense intensity",
                    61: "Rain: Slight",
                    63: "Rain: Moderate",
                    65: "Rain: Heavy intensity",
                    66: "Freezing Rain: Light",
                    67: "Freezing Rain: Heavy intensity",
                    71: "Snow fall: Slight",
                    73: "Snow fall: Moderate",
                    75: "Snow fall: Heavy intensity",
                    77: "Snow grains",
                    80: "Rain showers: Slight",
                    81: "Rain showers: Moderate",
                    82: "Rain showers: Violent",
                    85: "Snow showers slight",
                    86: "Snow showers heavy",
                    95: "Thunderstorm: Slight or moderate",
                    96: "Thunderstorm with slight hail",
                    99: "Thunderstorm with heavy hail",
                    }

                condition = weather_codes.get(code, "Unknown")
                forecast_items.append(
                    WeatherForecastItem(
                        time=time,
                        temperature_2m=temp,
                        precipitation=precip,
                        weathercode=code,
                    )
                 )

            return DailyWeatherForecast(forecast=forecast_items)
        except KeyError as e:
            raise ValueError(f"Unexpected API response structure for forecast. Missing key:{e}") from e
        except Exception as e:
            raise Exception(f"An error occurred while parsing the forecast data: {e}")

