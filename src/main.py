from fastapi import FastAPI
from src.api.v1 import community, raffle, notification
from src.core.config import settings
from src.core.logging import setup_logging

app = FastAPI(title="VK Randomizer API", docs_url="/docs", redoc_url="/redoc")

# Настройка логирования
setup_logging()

# Подключение роутов
app.include_router(community.router, prefix="/api/v1", tags=["Communities"])
app.include_router(raffle.router, prefix="/api/v1", tags=["Raffles"])
app.include_router(notification.router, prefix="/api/v1", tags=["Notifications"])

@app.get("/")
async def root():
    return {"message": "VK Randomizer API"}
