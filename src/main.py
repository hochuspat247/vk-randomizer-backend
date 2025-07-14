from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.api.v1 import community, raffle, notification, community_modal, nested_community_card, notification_card
from src.api.v1.raffle import raffle_cards_router
from src.api.v1.notification import settings_router
from src.core.config import settings
from src.core.logging import setup_logging

# Настройка метаданных для Swagger
app = FastAPI(
    title="VK Randomizer API",
    description="""
    ## API для управления розыгрышами в VK сообществах
    
    ### Основные возможности:
    - 🎯 Создание и управление розыгрышами
    - 👥 Управление сообществами
    - 🔔 Система уведомлений
    - 📊 Статистика и аналитика
    
    ### Розыгрыши
    Поддерживает создание розыгрышей с различными условиями участия:
    - Название и описание
    - Фотографии (до 5 шт)
    - Обязательные условия (подписка на сообщество, Telegram)
    - Партнерские теги
    - Черный список участников
    - Настройки завершения (по времени/участникам)
    - Дополнительные опции (скрыть количество участников, исключить администрацию)
    
    ### Авторизация
    API использует токены для аутентификации.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "VK Randomizer Team",
        "email": "support@vkrandomizer.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Настройка логирования
setup_logging()

# Подключение роутов
app.include_router(community.router, prefix="/api/v1", tags=["Communities"])
app.include_router(raffle.router, prefix="/api/v1", tags=["Raffles"])
app.include_router(notification.router, prefix="/api/v1", tags=["Notifications"])
app.include_router(community_modal.router, prefix="/api/v1", tags=["CommunityModals"])
app.include_router(nested_community_card.router, prefix="/api/v1", tags=["NestedCommunityCards"])
app.include_router(notification_card.router, prefix="/api/v1", tags=["NotificationCards"])
app.include_router(raffle_cards_router, prefix="/api/v1", tags=["RaffleCards"])
app.include_router(settings_router, prefix="/api/v1", tags=["NotificationSettings"])
app.mount("/photos", StaticFiles(directory="uploaded_photos"), name="photos")

@app.get("/", tags=["Root"])
async def root():
    """
    Корневой эндпоинт API.
    
    Возвращает основную информацию о сервисе.
    """
    return {
        "message": "VK Randomizer API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Проверка состояния сервиса.
    
    Используется для мониторинга работоспособности API.
    """
    return {"status": "healthy", "timestamp": "2025-01-18T12:00:00Z"}
