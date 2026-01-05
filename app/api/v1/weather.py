from fastapi import APIRouter, HTTPException, Query
from app.models.schemas import WeatherResponse
from app.services.weather import get_live_weather

router = APIRouter()

@router.get("/weather", response_model=WeatherResponse, response_model_by_alias=False)
async def read_weather(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    unit: str = Query("metric", enum=["metric", "imperial"], description="Unit system")
):
    try:
        return await get_live_weather(lat, lon, unit)
    except Exception as e:
        # In a real app, logs would go here
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather: {str(e)}")
