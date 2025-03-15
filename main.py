import flet as ft
from views.login_view import login_view
import asyncio
# import os - For if our API keys are env vars
from controllers.weather_controller import WeatherController

async def main(page: ft.Page):
    page.title = "Gardenia"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 420
    page.window_height = 850

    # Initialize WeatherController (defaults to Manila)
    weather_controller = WeatherController()

    # FOR TESTING, will add to views later
    try:
        current_weather = await weather_controller.get_current_weather()
        print(f"Current weather: {current_weather.condition}, {current_weather.temperature}°C, Precipitation: {current_weather.precipitation}mm")

        forecast = await weather_controller.get_weather_forecast()
        for item in forecast.forecast[:5]:
            print(f"{item.time}:  Temp: {item.temperature_2m}°C,  Precip: {item.precipitation}mm, condition: {item.weathercode}")

    except Exception as e:
        print(f"Error fetching weather: {e}")

    await login_view(page) # await for async

if __name__ == "__main__":
    ft.app(target=main)
