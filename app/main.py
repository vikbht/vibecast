from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.api.v1.weather import router as weather_router
from app.api.v1.music import router as music_router
from app.api.v1.shopping import router as shopping_router
from app.api.v1.dining import router as dining_router
import os

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(weather_router, prefix=settings.API_V1_STR)
app.include_router(music_router, prefix=f"{settings.API_V1_STR}/music")
app.include_router(shopping_router, prefix=f"{settings.API_V1_STR}/shopping")
app.include_router(dining_router, prefix=f"{settings.API_V1_STR}/dining")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root():
    return FileResponse(os.path.join("app", "static", "index.html"))

@app.get("/health")
async def health_check():
    return {"status": "ok"}
