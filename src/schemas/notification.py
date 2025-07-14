# Схемы для уведомлений

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime

class NotificationType(str, Enum):
    """Типы уведомлений"""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"

class NotificationBase(BaseModel):
    """Базовая схема для уведомлений"""
    type: NotificationType = Field(..., description="Тип уведомления")
    title: str = Field(..., min_length=1, max_length=200, description="Заголовок уведомления")
    message: str = Field(..., min_length=1, max_length=1000, description="Текст уведомления")
    is_read: bool = Field(default=False, description="Прочитано ли уведомление")

class NotificationCreate(NotificationBase):
    """Схема для создания уведомления"""
    id: int = Field(..., description="Уникальный идентификатор уведомления")
    created_at: str = Field(..., description="Дата и время создания уведомления в формате ISO")

class NotificationUpdate(BaseModel):
    """Схема для обновления уведомления"""
    type: Optional[NotificationType] = Field(None, description="Тип уведомления")
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Заголовок уведомления")
    message: Optional[str] = Field(None, min_length=1, max_length=1000, description="Текст уведомления")
    is_read: Optional[bool] = Field(None, description="Прочитано ли уведомление")

class Notification(NotificationBase):
    """Полная схема уведомления"""
    id: int = Field(..., description="Уникальный идентификатор уведомления")
    created_at: str = Field(..., description="Дата и время создания уведомления в формате ISO")

    class Config:
        """Конфигурация Pydantic"""
        json_schema_extra = {
            "example": {
                "id": 1,
                "type": "INFO",
                "title": "Розыгрыш завершен",
                "message": "Розыгрыш 'Технические новинки' успешно завершен. Победители определены.",
                "is_read": False,
                "created_at": "2025-01-18T10:30:00Z"
            }
        }

class UserNotificationSettings(BaseModel):
    win_notify: bool = True
    start_notify: bool = True
    finish_notify: bool = True
    widget_notify: bool = True
    banner: bool = True
    sound: bool = True
    dnd_until: Optional[datetime] = None

    class Config:
        from_attributes = True
