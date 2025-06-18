from pydantic import BaseModel, Field
from typing import List, Literal, Union, Optional

class CompletedNotificationCard(BaseModel):
    type: Literal["completed"] = Field(..., example="completed")
    raffleId: int = Field(..., example=38289)
    participantsCount: int = Field(..., example=5920)
    winners: List[str] = Field(..., example=["593IF", "REOOJ", "DOXO"])
    reasonEnd: str = Field(..., example="Достигнут лимит по числу участников.")
    new: bool = Field(..., example=True)

class WarningNotificationCard(BaseModel):
    type: Literal["warning"] = Field(..., example="warning")
    warningTitle: str = Field(..., example="Не удалось подключить виджет")
    warningDescription: List[str] = Field(..., example=[
        'Сообщество "Казань 24 – Новости"',
        'У пользователя недостаточно прав.',
        'Розыгрыш не запущен.'
    ])
    new: bool = Field(..., example=True)

class ErrorNotificationCard(BaseModel):
    type: Literal["error"] = Field(..., example="error")
    errorTitle: str = Field(..., example="Ошибка подключения сообщества")
    errorDescription: str = Field(..., example="На сервере VK ведутся технические работы. Приносим извинения за доставленные неудобства!")
    new: bool = Field(..., example=False)

NotificationCard = Union[
    CompletedNotificationCard,
    WarningNotificationCard,
    ErrorNotificationCard
]

class NotificationCardResponse(BaseModel):
    notification: NotificationCard

class NotificationCardListResponse(BaseModel):
    notifications: List[NotificationCard] 