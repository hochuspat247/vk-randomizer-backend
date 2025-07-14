from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
from datetime import datetime, timedelta
import uuid

from src.schemas.raffle import (
    RaffleCreate, 
    RaffleUpdate, 
    RaffleResponse, 
    RaffleListResponse
)

router = APIRouter(prefix="/raffles", tags=["Raffles"])

# In-memory demo DB
raffles_db: Dict[str, RaffleResponse] = {}

# Демо-данные
demo_raffles = [
    {
        "id": "492850",
        "name": "Конкурс на лучший пост о лете",
        "community_id": "1",
        "contest_text": "Поделитесь своими лучшими летними фотографиями и выиграйте призы! Условия участия: подписка на сообщество и лайк поста.",
        "photos": ["https://example.com/summer1.jpg", "https://example.com/summer2.jpg"],
        "require_community_subscription": True,
        "require_telegram_subscription": False,
        "telegram_channel": None,
        "required_communities": ["@techclub", "@mosnews24"],
        "partner_tags": ["@summer_partner"],
        "winners_count": 5,
        "blacklist_participants": ["@spam_user"],
        "start_date": datetime.now(),
        "end_date": datetime.now() + timedelta(days=30),
        "max_participants": 1000,
        "publish_results": True,
        "hide_participants_count": False,
        "exclude_me": False,
        "exclude_admins": False,
        "status": "active",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "participants_count": 127
    },
    {
        "id": "382189",
        "name": "Розыгрыш подарков к Новому году",
        "community_id": "2",
        "contest_text": "Новогодний розыгрыш! Подпишитесь на наш Telegram-канал и участвуйте в розыгрыше призов.",
        "photos": ["https://example.com/newyear1.jpg"],
        "require_community_subscription": True,
        "require_telegram_subscription": True,
        "telegram_channel": "@newyear_channel",
        "required_communities": ["@mosnews24"],
        "partner_tags": ["@gift_partner", "@holiday_partner"],
        "winners_count": 3,
        "blacklist_participants": [],
        "start_date": datetime.now() - timedelta(days=5),
        "end_date": datetime.now() + timedelta(days=25),
        "max_participants": 500,
        "publish_results": True,
        "hide_participants_count": True,
        "exclude_me": True,
        "exclude_admins": True,
        "status": "active",
        "created_at": datetime.now() - timedelta(days=5),
        "updated_at": datetime.now(),
        "participants_count": 89
    },
    {
        "id": "818394",
        "name": "Конкурс репостов",
        "community_id": "3",
        "contest_text": "Сделайте репост этого поста и участвуйте в розыгрыше! Простые условия участия.",
        "photos": ["https://example.com/repost1.jpg", "https://example.com/repost2.jpg", "https://example.com/repost3.jpg"],
        "require_community_subscription": True,
        "require_telegram_subscription": False,
        "telegram_channel": None,
        "required_communities": ["@kazan24"],
        "partner_tags": [],
        "winners_count": 10,
        "blacklist_participants": ["@bot1", "@bot2"],
        "start_date": datetime.now() - timedelta(days=10),
        "end_date": datetime.now() + timedelta(days=20),
        "max_participants": None,
        "publish_results": False,
        "hide_participants_count": False,
        "exclude_me": False,
        "exclude_admins": False,
        "status": "draft",
        "created_at": datetime.now() - timedelta(days=10),
        "updated_at": datetime.now() - timedelta(days=10),
        "participants_count": 0
    }
]

# Инициализация демо-данных
for raffle_data in demo_raffles:
    raffles_db[raffle_data["id"]] = RaffleResponse(**raffle_data)

@router.post("/", response_model=RaffleResponse, status_code=status.HTTP_201_CREATED, 
             summary="Создать новый розыгрыш",
             description="Создает новый розыгрыш с указанными параметрами")
async def create_raffle(raffle: RaffleCreate):
    """
    Создает новый розыгрыш.
    
    **Обязательные поля:**
    - `name` - Название розыгрыша
    - `community_id` - ID сообщества
    - `contest_text` - Текст конкурсного поста
    - `photos` - Список URL фотографий (до 5 шт)
    - `required_communities` - Теги обязательных сообществ
    - `winners_count` - Количество победителей (1-100)
    - `start_date` - Дата и время старта
    - `end_date` - Дата и время завершения
    """
    # Генерируем уникальный ID
    raffle_id = str(uuid.uuid4())
    
    # Создаем объект розыгрыша
    raffle_response = RaffleResponse(
        id=raffle_id,
        name=raffle.name,
        community_id=raffle.community_id,
        contest_text=raffle.contest_text,
        photos=raffle.photos,
        require_community_subscription=raffle.require_community_subscription,
        require_telegram_subscription=raffle.require_telegram_subscription,
        telegram_channel=raffle.telegram_channel,
        required_communities=raffle.required_communities,
        partner_tags=raffle.partner_tags,
        winners_count=raffle.winners_count,
        blacklist_participants=raffle.blacklist_participants,
        start_date=raffle.start_date,
        end_date=raffle.end_date,
        max_participants=raffle.max_participants,
        publish_results=raffle.publish_results,
        hide_participants_count=raffle.hide_participants_count,
        exclude_me=raffle.exclude_me,
        exclude_admins=raffle.exclude_admins,
        status="draft",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        participants_count=0
    )
    
    raffles_db[raffle_id] = raffle_response
    return raffle_response

@router.get("/", response_model=RaffleListResponse,
            summary="Получить список розыгрышей",
            description="Возвращает список розыгрышей с пагинацией и фильтрацией")
async def get_raffles():
    """
    Получает список розыгрышей с возможностью фильтрации и пагинации.
    """
    raffles = list(raffles_db.values())
    return RaffleListResponse(
        raffles=raffles,
        total=len(raffles),
        page=1,
        per_page=len(raffles)
    )

@router.get("/all", response_model=List[RaffleResponse],
            summary="Получить все розыгрыши",
            description="Возвращает все розыгрыши без пагинации и фильтров")
async def get_all_raffles_simple():
    """
    Получает все розыгрыши без пагинации и фильтров.
    
    **Возвращает:**
    - Список всех розыгрышей в системе
    """
    return list(raffles_db.values())

@router.get("/{raffle_id}", response_model=RaffleResponse,
            summary="Получить розыгрыш по ID",
            description="Возвращает детальную информацию о розыгрыше")
async def get_raffle(raffle_id: str):
    """
    Получает детальную информацию о розыгрыше по его ID.
    
    **Параметры:**
    - `raffle_id` - Уникальный идентификатор розыгрыша
    
    **Ошибки:**
    - `404` - Розыгрыш не найден
    """
    raffle = raffles_db.get(raffle_id)
    if not raffle:
        raise HTTPException(status_code=404, detail="Розыгрыш не найден")
    
    return raffle

@router.put("/{raffle_id}", response_model=RaffleResponse,
            summary="Обновить розыгрыш",
            description="Обновляет существующий розыгрыш")
async def update_raffle(raffle_id: str, raffle_update: RaffleUpdate):
    """
    Обновляет существующий розыгрыш.
    
    **Параметры:**
    - `raffle_id` - Уникальный идентификатор розыгрыша
    - `raffle_update` - Данные для обновления (все поля необязательны)
    
    **Ошибки:**
    - `404` - Розыгрыш не найден
    - `422` - Ошибка валидации данных
    """
    if raffle_id not in raffles_db:
        raise HTTPException(status_code=404, detail="Розыгрыш не найден")
    
    # Обновляем только переданные поля
    update_data = raffle_update.dict(exclude_unset=True)
    current_raffle = raffles_db[raffle_id]
    
    for field, value in update_data.items():
        setattr(current_raffle, field, value)
    
    current_raffle.updated_at = datetime.now()
    return current_raffle

@router.delete("/{raffle_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить розыгрыш",
               description="Удаляет розыгрыш по ID")
async def delete_raffle(raffle_id: str):
    """
    Удаляет розыгрыш по ID.
    
    **Параметры:**
    - `raffle_id` - Уникальный идентификатор розыгрыша
    
    **Ошибки:**
    - `404` - Розыгрыш не найден
    """
    if raffle_id not in raffles_db:
        raise HTTPException(status_code=404, detail="Розыгрыш не найден")
    
    del raffles_db[raffle_id]
    return None

@router.patch("/{raffle_id}/status", response_model=RaffleResponse,
              summary="Изменить статус розыгрыша",
              description="Изменяет статус розыгрыша (активировать, приостановить, завершить)")
async def change_raffle_status(raffle_id: str, status: str):
    """
    Изменяет статус розыгрыша.
    
    **Параметры:**
    - `raffle_id` - Уникальный идентификатор розыгрыша
    - `status` - Новый статус: draft, active, paused, completed, cancelled
    
    **Ошибки:**
    - `404` - Розыгрыш не найден
    - `400` - Недопустимое изменение статуса
    """
    if raffle_id not in raffles_db:
        raise HTTPException(status_code=404, detail="Розыгрыш не найден")
    
    raffle = raffles_db[raffle_id]
    
    # Проверяем допустимость изменения статуса
    if raffle.status == "completed" and status != "completed":
        raise HTTPException(status_code=400, detail="Нельзя изменить статус завершенного розыгрыша")
    
    raffle.status = status
    raffle.updated_at = datetime.now()
    return raffle 