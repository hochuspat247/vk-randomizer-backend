from pydantic import BaseModel, Field
from typing import Literal, Optional, List

class NestedCommunityCard(BaseModel):
    status: Optional[Literal["green", "yellow", "red"]] = Field(None, description="Статус виджета", example="green")
    statusText: str = Field(..., description="Текст статуса", example="Виджет настроен")
    name: str = Field(..., description="Название сообщества", example="Питер Онлайн")
    nickname: str = Field(..., description="Никнейм сообщества", example="@spbonline")
    adminType: Literal["owner", "admin"] = Field(..., description="Тип администратора", example="owner")
    membersCount: str = Field(..., description="Количество участников", example="1.2M")

class NestedCommunityCardListResponse(BaseModel):
    cards: List[NestedCommunityCard] 