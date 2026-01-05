from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "VibeCast"
    API_V1_STR: str = "/api/v1"
    WEATHER_API_BASE_URL: str = "https://api.open-meteo.com/v1"
    
    # Amazon PA-API
    AMAZON_ACCESS_KEY: str = ""
    AMAZON_SECRET_KEY: str = ""
    AMAZON_TAG: str = ""
    AMAZON_REGION: str = "US"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
