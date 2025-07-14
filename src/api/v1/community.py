from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Dict
from src.schemas.community import CommunityCard, CommunityCardCreate, CommunityCardUpdate
from src.utils.helpers import getRoleDisplayName

router = APIRouter(prefix="/communities", tags=["Communities"])

# In-memory demo DB
communities_db: Dict[str, CommunityCard] = {}

# Демо-данные
communities_db["1"] = CommunityCard(
    id="1",
    vk_user_id="123456",
    name="Техно-сообщество",
    nickname="@techclub",
    membersCount="12 500",
    raffleCount="8",
    adminType="owner",
    avatarUrl="https://example.com/avatar.jpg",
    status="green",
    buttonDesc="Последнее изменение: 14.10 21:31 – Администратор",
    stateText="Активен"
)
communities_db["2"] = CommunityCard(
    id="2",
    vk_user_id="123456",
    name="Москва 24 – Новости",
    nickname="@mosnews24",
    membersCount="522K",
    raffleCount="15",
    adminType="admin",
    avatarUrl="https://example.com/mosnews.jpg",
    status="yellow",
    buttonDesc="Последнее изменение: 15.10 14:20 – Модератор",
    stateText="Неактивен"
)
communities_db["3"] = CommunityCard(
    id="3",
    vk_user_id="654321",
    name="Казань 24 – Новости",
    nickname="@kazan24",
    membersCount="804K",
    raffleCount="12",
    adminType="owner",
    avatarUrl="https://example.com/kazan.jpg",
    status="red",
    buttonDesc="Последнее изменение: 16.10 09:15 – Администратор",
    stateText="Неактивен"
)
communities_db["4"] = CommunityCard(
    id="4",
    vk_user_id="654321",
    name="Санкт-Петербург Онлайн",
    nickname="@spbonline",
    membersCount="878K",
    raffleCount="20",
    adminType="admin",
    avatarUrl="https://example.com/spb.jpg",
    status="green",
    buttonDesc="Последнее изменение: 17.10 16:45 – Админ",
    stateText="Активен"
)

@router.get("/cards", response_model=List[CommunityCard], summary="Получить список карточек сообществ")
async def get_community_cards(vk_user_id: str = Query(..., description="VK user ID владельца")):
    """
    Возвращает список всех карточек сообществ, принадлежащих пользователю с указанным VK user ID.
    """
    result = []
    for c in communities_db.values():
        if c.vk_user_id == vk_user_id:
            card_dict = c.dict()
            card_dict["adminTypeDisplay"] = getRoleDisplayName(c.adminType)
            result.append(card_dict)
    return result

@router.get("/cards/{card_id}", response_model=CommunityCard, summary="Получить карточку сообщества по ID")
async def get_community_card(card_id: str):
    """
    Возвращает карточку сообщества по указанному ID.
    
    **Параметры:**
    - card_id: Уникальный идентификатор карточки (строка)
    
    **Возвращает:**
    - Карточка сообщества с полной информацией
    
    **Ошибки:**
    - 404: Карточка не найдена
    - 500: Ошибка сервера при получении данных
    
    **Пример ответа:**
    ```json
    {
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
    ```
    """
    community = communities_db.get(card_id)
    if not community:
        raise HTTPException(status_code=404, detail="Карточка не найдена")
    return community

@router.post("/cards", response_model=CommunityCard, status_code=status.HTTP_201_CREATED, summary="Создать карточку сообщества")
async def create_community_card(card: CommunityCardCreate):
    """
    Создает новую карточку сообщества в базе данных.
    
    **Параметры:**
    - card: Данные для создания карточки сообщества (обязательно все поля)
    
    **Возвращает:**
    - Созданная карточка сообщества
    
    **Ошибки:**
    - 400: Карточка с таким ID уже существует
    - 422: Ошибка валидации данных
    - 500: Ошибка сервера при создании
    
    **Пример запроса:**
    ```json
    {
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
    ```
    
    **Пример ответа:**
    ```json
    {
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
    ```
    """
    if card.id in communities_db:
        raise HTTPException(status_code=400, detail="Карточка с таким ID уже существует")
    communities_db[card.id] = CommunityCard(**card.dict())
    return communities_db[card.id]

@router.put("/cards/{card_id}", response_model=CommunityCard, summary="Обновить карточку сообщества")
async def update_community_card(card_id: str, card: CommunityCardUpdate):
    """
    Обновляет данные карточки сообщества по ID.
    
    **Параметры:**
    - card_id: Уникальный идентификатор карточки (строка)
    - card: Данные для обновления карточки (все поля необязательны)
    
    **Возвращает:**
    - Обновленная карточка сообщества
    
    **Ошибки:**
    - 404: Карточка не найдена
    - 422: Ошибка валидации данных
    - 500: Ошибка сервера при обновлении
    
    **Пример запроса:**
    ```json
    {
        "name": "Обновленное название",
        "membersCount": "15 000",
        "status": "yellow"
    }
    ```
    
    **Пример ответа:**
    ```json
    {
        "id": "1",
        "name": "Обновленное название",
        "nickname": "@techclub",
        "membersCount": "15 000",
        "raffleCount": "8",
        "adminType": "owner",
        "avatarUrl": "https://example.com/avatar.jpg",
        "status": "yellow",
        "buttonDesc": "Последнее изменение: 14.10 21:31 – Администратор",
        "stateText": "Активен"
    }
    ```
    """
    if card_id not in communities_db:
        raise HTTPException(status_code=404, detail="Карточка не найдена")
    
    current_card = communities_db[card_id]
    update_data = card.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(current_card, key, value)
    
    return current_card

@router.patch("/cards/{card_id}", response_model=CommunityCard, summary="Частично обновить карточку сообщества")
async def patch_community_card(card_id: str, card: CommunityCardUpdate):
    """
    Частично обновляет данные карточки сообщества по ID.
    
    **Параметры:**
    - card_id: Уникальный идентификатор карточки (строка)
    - card: Данные для частичного обновления карточки (любые поля)
    
    **Возвращает:**
    - Обновленная карточка сообщества
    
    **Ошибки:**
    - 404: Карточка не найдена
    - 422: Ошибка валидации данных
    - 500: Ошибка сервера при обновлении
    
    **Пример запроса:**
    ```json
    {
        "status": "red",
        "buttonDesc": "Новое описание кнопки"
    }
    ```
    
    **Пример ответа:**
    ```json
    {
        "id": "1",
        "name": "Техно-сообщество",
        "nickname": "@techclub",
        "membersCount": "12 500",
        "raffleCount": "8",
        "adminType": "owner",
        "avatarUrl": "https://example.com/avatar.jpg",
        "status": "red",
        "buttonDesc": "Новое описание кнопки",
        "stateText": "Активен"
    }
    ```
    """
    if card_id not in communities_db:
        raise HTTPException(status_code=404, detail="Карточка не найдена")
    
    current_card = communities_db[card_id]
    update_data = card.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(current_card, key, value)
    
    return current_card

@router.delete("/cards/{card_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить карточку сообщества")
async def delete_community_card(card_id: str):
    """
    Удаляет карточку сообщества по ID.
    
    **Параметры:**
    - card_id: Уникальный идентификатор карточки (строка)
    
    **Возвращает:**
    - 204: Карточка успешно удалена
    
    **Ошибки:**
    - 404: Карточка не найдена
    - 500: Ошибка сервера при удалении
    
    **Пример использования:**
    ```
    DELETE /api/v1/communities/cards/1
    ```
    
    **Ответ:**
    ```
    HTTP/1.1 204 No Content
    ```
    """
    if card_id not in communities_db:
        raise HTTPException(status_code=404, detail="Карточка не найдена")
    del communities_db[card_id]
    return None