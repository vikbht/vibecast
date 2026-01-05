import httpx
from app.core.config import settings
from app.models.schemas import WeatherResponse

async def get_live_weather(lat: float, lon: float, unit: str = "metric") -> WeatherResponse:
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m,weather_code"
    }

    if unit == "imperial":
        params["temperature_unit"] = "fahrenheit"
        params["wind_speed_unit"] = "mph"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.WEATHER_API_BASE_URL}/forecast",
            params=params
        )
        response.raise_for_status()
        data = response.json()
        return WeatherResponse(**data)
