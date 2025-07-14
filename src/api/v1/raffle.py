# Эндпоинты для работы с розыгрышами

from fastapi import APIRouter, HTTPException, status, Depends, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime
import enum
import shutil
import os

from src.db.session import get_db
from src.db.models.raffle import Raffle, RaffleStatus
from src.schemas.raffle import (
    RaffleCreate, 
    RaffleUpdate, 
    RaffleResponse, 
    RaffleListResponse
)

router = APIRouter(prefix="/raffles", tags=["Raffles"])
# Новый роутер-алиас для raffle-cards
raffle_cards_router = APIRouter(prefix="/raffle-cards", tags=["RaffleCards"])

UPLOAD_DIR = "uploaded_photos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=RaffleResponse, status_code=status.HTTP_201_CREATED, 
             summary="Создать новый розыгрыш",
             description="Создает новый розыгрыш с указанными параметрами")
async def create_raffle(
    raffle: RaffleCreate,
    db: Session = Depends(get_db)
):
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
    
    **Пример запроса:**
    ```json
    {
        "name": "Конкурс на лучший пост",
        "community_id": "12345",
        "contest_text": "Участвуйте в нашем конкурсе!",
        "photos": ["https://example.com/photo1.jpg"],
        "require_community_subscription": true,
        "require_telegram_subscription": false,
        "required_communities": ["@community1", "@community2"],
        "partner_tags": ["@partner1"],
        "winners_count": 5,
        "blacklist_participants": ["@user1"],
        "start_date": "2025-07-09T14:33:00",
        "end_date": "2025-08-09T11:33:00",
        "max_participants": 1000,
        "publish_results": true,
        "hide_participants_count": false,
        "exclude_me": false,
        "exclude_admins": false
    }
    ```
    """
    # Генерируем уникальный ID
    raffle_id = str(uuid.uuid4())
    
    # Создаем объект розыгрыша
    db_raffle = Raffle(
        id=raffle_id,
        vk_user_id=raffle.vk_user_id,
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
        status=RaffleStatus.DRAFT
    )
    
    db.add(db_raffle)
    db.commit()
    db.refresh(db_raffle)

    raffle_dict = db_raffle.__dict__.copy()
    if isinstance(raffle_dict["status"], enum.Enum):
        raffle_dict["status"] = raffle_dict["status"].value
    return RaffleResponse(**raffle_dict)

@router.get("/", response_model=RaffleListResponse,
            summary="Получить список розыгрышей",
            description="Возвращает список розыгрышей с пагинацией и фильтрацией")
async def get_raffles(
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(10, ge=1, le=100, description="Количество элементов на странице"),
    status: Optional[RaffleStatus] = Query(None, description="Фильтр по статусу"),
    community_id: Optional[str] = Query(None, description="Фильтр по ID сообщества"),
    vk_user_id: Optional[str] = Query(None, description="Фильтр по VK user ID владельца"),
    db: Session = Depends(get_db)
):
    """
    Получает список розыгрышей с возможностью фильтрации и пагинации.
    
    **Параметры:**
    - `page` - Номер страницы (начиная с 1)
    - `per_page` - Количество элементов на странице (1-100)
    - `status` - Фильтр по статусу розыгрыша
    - `community_id` - Фильтр по ID сообщества
    
    **Примеры запросов:**
    - `GET /raffles/` - Все розыгрыши
    - `GET /raffles/?status=active` - Только активные розыгрыши
    - `GET /raffles/?community_id=12345` - Розыгрыши конкретного сообщества
    - `GET /raffles/?page=2&per_page=20` - Вторая страница по 20 элементов
    """
    query = db.query(Raffle)
    
    if status:
        query = query.filter(Raffle.status == status)
    if community_id:
        query = query.filter(Raffle.community_id == community_id)
    if vk_user_id:
        query = query.filter(Raffle.vk_user_id == vk_user_id)
    
    total = query.count()
    raffles = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return RaffleListResponse(
        raffles=[RaffleResponse.from_orm(raffle) for raffle in raffles],
        total=total,
        page=page,
        per_page=per_page
    )

@router.get("/all", response_model=List[RaffleResponse],
            summary="Получить все розыгрыши",
            description="Возвращает все розыгрыши без пагинации и фильтров")
async def get_all_raffles_simple(
    vk_user_id: Optional[str] = Query(None, description="Фильтр по VK user ID владельца"),
    db: Session = Depends(get_db)
):
    """
    Получает все розыгрыши без пагинации и фильтров.
    
    **Возвращает:**
    - Список всех розыгрышей в системе
    
    **Пример ответа:**
    ```json
    [
        {
            "id": "492850",
            "name": "Конкурс на лучший пост о лете",
            "community_id": "1",
            "contest_text": "Поделитесь своими лучшими летними фотографиями...",
            "photos": ["https://example.com/summer1.jpg"],
            "require_community_subscription": true,
            "require_telegram_subscription": false,
            "telegram_channel": null,
            "required_communities": ["@techclub", "@mosnews24"],
            "partner_tags": ["@summer_partner"],
            "winners_count": 5,
            "blacklist_participants": ["@spam_user"],
            "start_date": "2025-07-09T14:33:00",
            "end_date": "2025-08-09T11:33:00",
            "max_participants": 1000,
            "publish_results": true,
            "hide_participants_count": false,
            "exclude_me": false,
            "exclude_admins": false,
            "status": "active",
            "created_at": "2025-07-09T14:33:00",
            "updated_at": "2025-07-09T14:33:00",
            "participants_count": 127
        }
    ]
    ```
    """
    query = db.query(Raffle)
    if vk_user_id:
        query = query.filter(Raffle.vk_user_id == vk_user_id)
    raffles = query.all()
    return [RaffleResponse.from_orm(raffle) for raffle in raffles]

@router.get("/{raffle_id}", response_model=RaffleResponse,
            summary="Получить розыгрыш по ID",
            description="Возвращает детальную информацию о розыгрыше")
async def get_raffle(
    raffle_id: str,
    db: Session = Depends(get_db)
):
    """
    Получает детальную информацию о розыгрыше по его ID.
    
    **Параметры:**
    - `raffle_id` - Уникальный идентификатор розыгрыша
    
    **Ошибки:**
    - `404` - Розыгрыш не найден
    """
    raffle = db.query(Raffle).filter(Raffle.id == raffle_id).first()
    if not raffle:
        raise HTTPException(status_code=404, detail="Розыгрыш не найден")
    
    return RaffleResponse.from_orm(raffle)

@router.put("/{raffle_id}", response_model=RaffleResponse,
            summary="Обновить розыгрыш",
            description="Обновляет существующий розыгрыш")
async def update_raffle(
    raffle_id: str,
    raffle_update: RaffleUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновляет существующий розыгрыш.
    
    **Параметры:**
    - `raffle_id` - Уникальный идентификатор розыгрыша
    - `raffle_update` - Данные для обновления (все поля необязательны)
    
    **Ошибки:**
    - `404` - Розыгрыш не найден
    - `422` - Ошибка валидации данных
    """
    db_raffle = db.query(Raffle).filter(Raffle.id == raffle_id).first()
    if not db_raffle:
        raise HTTPException(status_code=404, detail="Розыгрыш не найден")
    
    # Обновляем только переданные поля
    update_data = raffle_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_raffle, field, value)
    
    db_raffle.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_raffle)
    
    return RaffleResponse.from_orm(db_raffle)

@router.delete("/{raffle_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить розыгрыш",
               description="Удаляет розыгрыш по ID")
async def delete_raffle(
    raffle_id: str,
    db: Session = Depends(get_db)
):
    """
    Удаляет розыгрыш по ID.
    
    **Параметры:**
    - `raffle_id` - Уникальный идентификатор розыгрыша
    
    **Ошибки:**
    - `404` - Розыгрыш не найден
    """
    db_raffle = db.query(Raffle).filter(Raffle.id == raffle_id).first()
    if not db_raffle:
        raise HTTPException(status_code=404, detail="Розыгрыш не найден")
    
    db.delete(db_raffle)
    db.commit()
    
    return None

@router.patch("/{raffle_id}/status", response_model=RaffleResponse,
              summary="Изменить статус розыгрыша",
              description="Изменяет статус розыгрыша (активировать, приостановить, завершить)")
async def change_raffle_status(
    raffle_id: str,
    status: RaffleStatus,
    db: Session = Depends(get_db)
):
    """
    Изменяет статус розыгрыша.
    
    **Параметры:**
    - `raffle_id` - Уникальный идентификатор розыгрыша
    - `status` - Новый статус: draft, active, paused, completed, cancelled
    
    **Ошибки:**
    - `404` - Розыгрыш не найден
    - `400` - Недопустимое изменение статуса
    """
    db_raffle = db.query(Raffle).filter(Raffle.id == raffle_id).first()
    if not db_raffle:
        raise HTTPException(status_code=404, detail="Розыгрыш не найден")
    
    # Проверяем допустимость изменения статуса
    if db_raffle.status == RaffleStatus.COMPLETED and status != RaffleStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Нельзя изменить статус завершенного розыгрыша")
    
    db_raffle.status = status
    db_raffle.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_raffle)
    
    return RaffleResponse.from_orm(db_raffle)

# Дублируем основные эндпоинты для raffle-cards
@raffle_cards_router.post("/", response_model=RaffleResponse, status_code=status.HTTP_201_CREATED, summary="Создать новый розыгрыш (алиас)")
async def create_raffle_card(
    raffle: RaffleCreate,
    db: Session = Depends(get_db)
):
    return await create_raffle(raffle, db)

@raffle_cards_router.get("/", response_model=RaffleListResponse, summary="Получить список розыгрышей (алиас)")
async def get_raffle_cards(
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(10, ge=1, le=100, description="Количество элементов на странице"),
    status: Optional[RaffleStatus] = Query(None, description="Фильтр по статусу"),
    community_id: Optional[str] = Query(None, description="Фильтр по ID сообщества"),
    vk_user_id: Optional[str] = Query(None, description="Фильтр по VK user ID владельца"),
    db: Session = Depends(get_db)
):
    return await get_raffles(page, per_page, status, community_id, vk_user_id, db)

@raffle_cards_router.get("/{raffle_id}", response_model=RaffleResponse, summary="Получить розыгрыш по ID (алиас)")
async def get_raffle_card_by_id(
    raffle_id: str,
    db: Session = Depends(get_db)
):
    return await get_raffle(raffle_id, db)

@raffle_cards_router.put("/{raffle_id}", response_model=RaffleResponse, summary="Обновить розыгрыш (алиас)")
async def update_raffle_card(
    raffle_id: str,
    raffle_update: RaffleUpdate,
    db: Session = Depends(get_db)
):
    return await update_raffle(raffle_id, raffle_update, db)

@raffle_cards_router.post("/upload-photo/", summary="Загрузить фото для розыгрыша")
async def upload_raffle_photo(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"url": f"/photos/{file.filename}"}
