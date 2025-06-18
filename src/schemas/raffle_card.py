from pydantic import BaseModel, Field
from typing import Literal, Optional, List

class RaffleCard(BaseModel):
    raffleId: str = Field(..., description="ID розыгрыша", example="492850")
    name: str = Field(..., description="Название сообщества", example="Казань 24 – Новости")
    textRaffleState: str = Field(..., description="Состояние розыгрыша", example="Активно")
    winnersCount: int = Field(..., description="Количество победителей", example=5)
    mode: Literal["both", "time", "members"] = Field(..., description="Режим розыгрыша", example="both")
    memberCount: Optional[str] = Field(None, description="Количество участников (для режима members/both)", example="27")
    timeLeft: Optional[str] = Field(None, description="Оставшееся время (для режима time/both)", example="2Д 9Ч 21М")
    progress: int = Field(..., description="Прогресс розыгрыша в процентах", example=99)
    lastModified: str = Field(..., description="Дата последнего изменения", example="14.10.2025 21:31")
    modifiedBy: str = Field(..., description="Кто изменил", example="Администратор")
    statusСommunity: Literal["error", "connected", "notConfig"] = Field(..., description="Статус сообщества", example="error")
    statusNestedCard: Literal["green", "yellow", "red"] = Field(..., description="Статус вложенной карточки", example="green")
    statusNestedText: str = Field(..., description="Текст статуса вложенной карточки", example="Недостаточно прав")
    nickname: str = Field(..., description="Никнейм сообщества", example="@mosnews24")
    membersCountNested: str = Field(..., description="Количество участников вложенной карточки", example="522K")
    adminType: Literal["owner", "admin"] = Field(..., description="Тип администратора", example="admin")

class RaffleCardResponse(BaseModel):
    raffle: RaffleCard

class RaffleCardListResponse(BaseModel):
    raffles: List[RaffleCard] 