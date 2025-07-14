from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
from datetime import datetime
from enum import Enum

class RaffleCreate(BaseModel):
    """Схема для создания розыгрыша"""
    vk_user_id: str = Field(..., description="VK user ID владельца", example="123456")
    name: str = Field(..., description="Название розыгрыша", example="Конкурс на лучший пост")
    community_id: str = Field(..., description="ID сообщества", example="12345")
    contest_text: str = Field(..., description="Текст конкурсного поста", example="Участвуйте в нашем конкурсе!")
    photos: List[str] = Field(..., description="Список URL фотографий (до 5 шт)", max_items=5, example=["https://example.com/photo1.jpg"])
    
    # Обязательные условия участия
    require_community_subscription: bool = Field(True, description="Подписка на сообщество")
    require_telegram_subscription: bool = Field(False, description="Подписка на Telegram-канал")
    telegram_channel: Optional[str] = Field(None, description="Telegram-канал", example="@my_channel")
    required_communities: List[str] = Field(..., description="Теги обязательных сообществ", example=["@community1", "@community2"])
    partner_tags: List[str] = Field(default=[], description="Теги партнеров", example=["@partner1"])
    
    # Основные параметры
    winners_count: int = Field(..., description="Количество победителей", ge=1, le=100, example=5)
    blacklist_participants: List[str] = Field(default=[], description="Черный список участников", example=["@user1", "@user2"])
    
    # Условия завершения
    start_date: datetime = Field(..., description="Дата и время старта розыгрыша", example="2025-07-09T14:33:00")
    end_date: datetime = Field(..., description="Дата и время завершения розыгрыша", example="2025-08-09T11:33:00")
    max_participants: Optional[int] = Field(None, description="Максимальное количество участников", ge=1, example=1000)
    
    # Дополнительные настройки
    publish_results: bool = Field(True, description="Опубликовать пост с итогами")
    hide_participants_count: bool = Field(False, description="Скрыть количество участников")
    exclude_me: bool = Field(False, description="Не учитывать в розыгрыше меня")
    exclude_admins: bool = Field(False, description="Не учитывать в розыгрыше администрацию сообщества")
    
    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('Дата завершения должна быть позже даты старта')
        return v
    
    @validator('photos')
    def validate_photos_count(cls, v):
        if len(v) > 5:
            raise ValueError('Максимальное количество фотографий - 5')
        return v

class RaffleUpdate(BaseModel):
    """Схема для обновления розыгрыша"""
    vk_user_id: Optional[str] = Field(None, description="VK user ID владельца", example="123456")
    name: Optional[str] = Field(None, description="Название розыгрыша")
    community_id: Optional[str] = Field(None, description="ID сообщества")
    contest_text: Optional[str] = Field(None, description="Текст конкурсного поста")
    photos: Optional[List[str]] = Field(None, description="Список URL фотографий (до 5 шт)", max_items=5)
    
    # Обязательные условия участия
    require_community_subscription: Optional[bool] = Field(None, description="Подписка на сообщество")
    require_telegram_subscription: Optional[bool] = Field(None, description="Подписка на Telegram-канал")
    telegram_channel: Optional[str] = Field(None, description="Telegram-канал")
    required_communities: Optional[List[str]] = Field(None, description="Теги обязательных сообществ")
    partner_tags: Optional[List[str]] = Field(None, description="Теги партнеров")
    
    # Основные параметры
    winners_count: Optional[int] = Field(None, description="Количество победителей", ge=1, le=100)
    blacklist_participants: Optional[List[str]] = Field(None, description="Черный список участников")
    
    # Условия завершения
    start_date: Optional[datetime] = Field(None, description="Дата и время старта розыгрыша")
    end_date: Optional[datetime] = Field(None, description="Дата и время завершения розыгрыша")
    max_participants: Optional[int] = Field(None, description="Максимальное количество участников", ge=1)
    
    # Дополнительные настройки
    publish_results: Optional[bool] = Field(None, description="Опубликовать пост с итогами")
    hide_participants_count: Optional[bool] = Field(None, description="Скрыть количество участников")
    exclude_me: Optional[bool] = Field(None, description="Не учитывать в розыгрыше меня")
    exclude_admins: Optional[bool] = Field(None, description="Не учитывать в розыгрыше администрацию сообщества")

class RaffleStatus(str, Enum):
    draft = "draft"
    active = "active"
    paused = "paused"
    completed = "completed"
    cancelled = "cancelled"

class RaffleResponse(BaseModel):
    """Схема для ответа с данными розыгрыша"""
    id: str = Field(..., description="ID розыгрыша")
    vk_user_id: str = Field(..., description="VK user ID владельца", example="123456")
    name: str = Field(..., description="Название розыгрыша")
    community_id: str = Field(..., description="ID сообщества")
    contest_text: str = Field(..., description="Текст конкурсного поста")
    photos: List[str] = Field(..., description="Список URL фотографий")
    
    # Обязательные условия участия
    require_community_subscription: bool = Field(..., description="Подписка на сообщество")
    require_telegram_subscription: bool = Field(..., description="Подписка на Telegram-канал")
    telegram_channel: Optional[str] = Field(None, description="Telegram-канал")
    required_communities: List[str] = Field(..., description="Теги обязательных сообществ")
    partner_tags: List[str] = Field(..., description="Теги партнеров")
    
    # Основные параметры
    winners_count: int = Field(..., description="Количество победителей")
    blacklist_participants: List[str] = Field(..., description="Черный список участников")
    
    # Условия завершения
    start_date: datetime = Field(..., description="Дата и время старта розыгрыша")
    end_date: datetime = Field(..., description="Дата и время завершения розыгрыша")
    max_participants: Optional[int] = Field(None, description="Максимальное количество участников")
    
    # Дополнительные настройки
    publish_results: bool = Field(..., description="Опубликовать пост с итогами")
    hide_participants_count: bool = Field(..., description="Скрыть количество участников")
    exclude_me: bool = Field(..., description="Не учитывать в розыгрыше меня")
    exclude_admins: bool = Field(..., description="Не учитывать в розыгрыше администрацию сообщества")
    
    # Статус и метаданные
    status: RaffleStatus = Field(..., description="Статус розыгрыша")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата последнего обновления")
    participants_count: int = Field(0, description="Количество участников")
    
    class Config:
        from_attributes = True

class RaffleListResponse(BaseModel):
    """Схема для списка розыгрышей"""
    raffles: List[RaffleResponse]
    total: int = Field(..., description="Общее количество розыгрышей")
    page: int = Field(..., description="Номер страницы")
    per_page: int = Field(..., description="Количество элементов на странице")
