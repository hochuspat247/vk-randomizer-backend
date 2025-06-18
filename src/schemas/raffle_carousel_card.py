from pydantic import BaseModel, Field
from typing import Literal, List

class RaffleCarouselCard(BaseModel):
    raffleId: str = Field(..., description="ID розыгрыша", example="1001")
    name: str = Field(..., description="Название сообщества", example="Москва 24 – Новости")
    status: Literal["active", "pending", "draft", "results", "deleted", "resultsWhite", "completed"] = Field(
        ..., 
        description="Статус розыгрыша", 
        example="active"
    )
    stateText: str = Field(..., description="Текст состояния", example="Активно")
    members: str = Field(..., description="Количество участников", example="4 280 участников")
    endDate: str = Field(..., description="Дата окончания", example="18.05 19:00")
    updatedAt: str = Field(..., description="Дата последнего обновления", example="17.05.2025 16:42")

class RaffleCarouselCardResponse(BaseModel):
    raffle: RaffleCarouselCard

class RaffleCarouselCardListResponse(BaseModel):
    raffles: List[RaffleCarouselCard] 