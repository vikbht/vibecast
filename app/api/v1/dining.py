from fastapi import APIRouter, Query
from app.services.dining import get_dining_recommendations
from app.models.schemas import DiningResponse

router = APIRouter()

@router.get("/recommend", response_model=DiningResponse)
def recommend_dining(
    city: str = Query(..., description="Name of the city"),
    preference: str = Query(None, description="Optional cuisine preference")
):
    return get_dining_recommendations(preference, city)
