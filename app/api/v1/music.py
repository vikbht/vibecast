from fastapi import APIRouter, Query
from app.services.music import get_music_recommendation
from app.models.schemas import MusicResponse

router = APIRouter()

@router.get("/recommend", response_model=MusicResponse)
def recommend_music(
    temperature: float = Query(..., description="Current temperature in Celsius"),
    weather_code: int = Query(..., description="WMO Weather code")
):
    return get_music_recommendation(temperature, weather_code)
