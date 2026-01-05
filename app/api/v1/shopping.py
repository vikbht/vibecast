from fastapi import APIRouter, Query
from app.services.shopping import get_shopping_recommendation
from app.models.schemas import ShoppingResponse
from datetime import datetime

router = APIRouter()

@router.get("/recommend", response_model=ShoppingResponse)
def recommend_shopping(
    temperature: float = Query(..., description="Current temperature in Celsius"),
    weather_code: int = Query(..., description="WMO Weather code"),
    hour: int = Query(None, description="Current hour at location (0-23)")
):
    # Determine current hour for day/night logic
    if hour is None:
        hour = datetime.now().hour
    
    return get_shopping_recommendation(temperature, weather_code, hour)
