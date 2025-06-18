from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Union

class SelectModal(BaseModel):
    id: str = Field(..., example="selectMock")
    type: Literal["select"] = Field(..., example="select")
    placeholder: str = Field(..., example="Выберите сообщество")
    options: List[str] = Field(..., example=["Казань 24 – Новости", "Москва Life", "Краснодар Online"])

class Subscriber(BaseModel):
    name: str = Field(..., example="Андрей")
    avatar: str = Field(..., example="https://example.com/avatar.jpg")

class PermissionModal(BaseModel):
    id: str = Field(..., example="permissionMock")
    type: Literal["permission"] = Field(..., example="permission")
    communityName: str = Field(..., example="Казань 24 – Новости")
    communityAvatar: str = Field(..., example="https://example.com/avatar.jpg")
    subscribers: List[Subscriber] = Field(..., example=[{"name": "Андрей", "avatar": "https://example.com/avatar.jpg"}])

class SuccessModal(BaseModel):
    id: str = Field(..., example="successMock")
    type: Literal["success"] = Field(..., example="success")
    communityName: str = Field(..., example="Казань 24 – Новости")
    communityAvatar: str = Field(..., example="https://example.com/avatar.jpg")

CommunityModal = Union[SelectModal, PermissionModal, SuccessModal]

class CommunityModalResponse(BaseModel):
    modal: CommunityModal

class CommunityModalListResponse(BaseModel):
    modals: List[CommunityModal] 