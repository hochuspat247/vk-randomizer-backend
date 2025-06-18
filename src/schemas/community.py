from pydantic import BaseModel, Field
from typing import Literal, Optional

class CommunityCardBase(BaseModel):
    name: str = Field(..., description="Название сообщества", example="Техно-сообщество")
    nickname: str = Field(..., description="Никнейм сообщества (с символом @)", example="@techclub")
    membersCount: str = Field(..., description="Количество участников", example="12 500")
    raffleCount: str = Field(..., description="Количество розыгрышей", example="8")
    adminType: Literal["owner", "admin"] = Field(..., description="Тип администратора", example="owner")
    avatarUrl: str = Field(..., description="URL аватара сообщества", example="https://example.com/avatar.jpg")
    status: Literal["yellow", "green", "red"] = Field(..., description="Статус сообщества", example="green")
    buttonDesc: str = Field(..., description="Описание кнопки/последние изменения", example="Последнее изменение: 14.10 21:31 – Администратор")
    stateText: Literal["Активен", "Неактивен"] = Field(..., description="Текст состояния", example="Активен")

class CommunityCardCreate(CommunityCardBase):
    id: str = Field(..., description="Уникальный идентификатор карточки", example="1")

class CommunityCardUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Название сообщества", example="Техно-сообщество")
    nickname: Optional[str] = Field(None, description="Никнейм сообщества (с символом @)", example="@techclub")
    membersCount: Optional[str] = Field(None, description="Количество участников", example="12 500")
    raffleCount: Optional[str] = Field(None, description="Количество розыгрышей", example="8")
    adminType: Optional[Literal["owner", "admin"]] = Field(None, description="Тип администратора", example="owner")
    avatarUrl: Optional[str] = Field(None, description="URL аватара сообщества", example="https://example.com/avatar.jpg")
    status: Optional[Literal["yellow", "green", "red"]] = Field(None, description="Статус сообщества", example="green")
    buttonDesc: Optional[str] = Field(None, description="Описание кнопки/последние изменения", example="Последнее изменение: 14.10 21:31 – Администратор")
    stateText: Optional[Literal["Активен", "Неактивен"]] = Field(None, description="Текст состояния", example="Активен")

class CommunityCard(CommunityCardBase):
    id: str = Field(..., description="Уникальный идентификатор карточки", example="1")

    class Config:
        from_attributes = True  # Поддержка преобразования из моделей SQLAlchemy
        json_schema_extra = {
            "example": {
                "id": "1",
                "name": "Техно-сообщество",
                "nickname": "@techclub",
                "membersCount": "12 500",
                "raffleCount": "8",
                "adminType": "owner",
                "avatarUrl": "https://example.com/avatar.jpg",
                "status": "green",
                "buttonDesc": "Последнее изменение: 14.10 21:31 – Администратор",
                "stateText": "Активен"
            }
        }