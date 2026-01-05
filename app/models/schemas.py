from pydantic import BaseModel, Field

class WeatherCurrent(BaseModel):
    temperature: float = Field(alias="temperature_2m")
    wind_speed: float = Field(alias="wind_speed_10m")
    weather_code: int = Field(alias="weather_code")
    time: str

class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    timezone: str
    current: WeatherCurrent
    
class MusicResponse(BaseModel):
    video_id: str
    title: str
    artist: str

    mood: str

class ShoppingItem(BaseModel):
    title: str
    price: str
    image_url: str
    product_url: str

class ShoppingResponse(BaseModel):
    items: list[ShoppingItem]
    mood: str

class DiningItem(BaseModel):
    name: str
    cuisine: str
    rating: float
    price_level: str
    image_url: str
    location: str

class DiningResponse(BaseModel):
    items: list[DiningItem]
    city: str
