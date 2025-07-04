from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1 import community_modal, nested_community_card, notification_card, raffle_card, raffle_carousel_card
from src.core.config import settings

app = FastAPI(title="VK Randomizer API", docs_url="/docs", redoc_url="/redoc")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Подключение роутов (только те, которые работают с in-memory данными)
app.include_router(community_modal.router, prefix="/api/v1", tags=["CommunityModals"])
app.include_router(nested_community_card.router, prefix="/api/v1", tags=["NestedCommunityCards"])
app.include_router(notification_card.router, prefix="/api/v1", tags=["NotificationCards"])
app.include_router(raffle_card.router, prefix="/api/v1", tags=["RaffleCards"])
app.include_router(raffle_carousel_card.router, prefix="/api/v1", tags=["RaffleCarouselCards"])

@app.get("/")
async def root():
    return {"message": "VK Randomizer API - Simplified Version"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"} 