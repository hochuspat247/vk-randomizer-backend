from fastapi import FastAPI
from src.api.v1 import community, raffle, notification, community_modal, nested_community_card, notification_card, raffle_card, raffle_carousel_card
from src.core.config import settings
from src.core.logging import setup_logging

app = FastAPI(title="VK Randomizer API", docs_url="/docs", redoc_url="/redoc")

# Настройка логирования
setup_logging()

# Подключение роутов
app.include_router(community.router, prefix="/api/v1", tags=["Communities"])
app.include_router(raffle.router, prefix="/api/v1", tags=["Raffles"])
app.include_router(notification.router, prefix="/api/v1", tags=["Notifications"])
app.include_router(community_modal.router, prefix="/api/v1", tags=["CommunityModals"])
app.include_router(nested_community_card.router, prefix="/api/v1", tags=["NestedCommunityCards"])
app.include_router(notification_card.router, prefix="/api/v1", tags=["NotificationCards"])
app.include_router(raffle_card.router, prefix="/api/v1", tags=["RaffleCards"])
app.include_router(raffle_carousel_card.router, prefix="/api/v1", tags=["RaffleCarouselCards"])

@app.get("/")
async def root():
    return {"message": "VK Randomizer API"}
