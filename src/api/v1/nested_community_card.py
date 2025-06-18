from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
from src.schemas.nested_community_card import NestedCommunityCard, NestedCommunityCardListResponse

router = APIRouter(prefix="/nested-community-cards", tags=["NestedCommunityCards"])

# In-memory demo DB
cards_db: Dict[str, NestedCommunityCard] = {}

def _make_id(card: NestedCommunityCard) -> str:
    return f"{card.nickname}"  # Можно заменить на uuid или другое поле

# Демо-данные
cards_db["@mosnews24"] = NestedCommunityCard(
    status=None,
    statusText="Статус неизвестен",
    name="Москва 24 – Новости",
    nickname="@mosnews24",
    adminType="admin",
    membersCount="592K"
)
cards_db["@spbonline"] = NestedCommunityCard(
    status="green",
    statusText="Виджет настроен",
    name="Питер Онлайн",
    nickname="@spbonline",
    adminType="owner",
    membersCount="1.2M"
)
cards_db["@kazan24"] = NestedCommunityCard(
    status="red",
    statusText="Ошибка подключения",
    name="Казань 24",
    nickname="@kazan24",
    adminType="admin",
    membersCount="804K"
)
cards_db["@nsknews"] = NestedCommunityCard(
    status="yellow",
    statusText="Требуется разрешение",
    name="Новосибирск – Главное",
    nickname="@nsknews",
    adminType="owner",
    membersCount="325K"
)

@router.get("/", response_model=NestedCommunityCardListResponse, summary="Получить все NestedCommunityCard")
async def get_all_cards():
    """
    Возвращает список всех вложенных карточек сообществ.
    
    **Возвращает:**
    - Список всех вложенных карточек сообществ
    
    **Примеры ответов:**
    - 200: Успешно получен список карточек
    - 500: Ошибка сервера при получении данных
    
    **Пример ответа:**
    ```json
    {
      "cards": [
        {
          "status": "green",
          "statusText": "Виджет настроен",
          "name": "Питер Онлайн",
          "nickname": "@spbonline",
          "adminType": "owner",
          "membersCount": "1.2M"
        },
        {
          "status": "red",
          "statusText": "Ошибка подключения",
          "name": "Казань 24",
          "nickname": "@kazan24",
          "adminType": "admin",
          "membersCount": "804K"
        }
      ]
    }
    ```
    """
    return {"cards": list(cards_db.values())}

@router.get("/{nickname}", response_model=NestedCommunityCard, summary="Получить NestedCommunityCard по nickname")
async def get_card(nickname: str):
    """
    Возвращает вложенную карточку сообщества по nickname.
    
    **Параметры:**
    - nickname: Никнейм сообщества (строка, начинается с @)
    
    **Возвращает:**
    - Вложенная карточка сообщества с полной информацией
    
    **Ошибки:**
    - 404: Карточка не найдена
    - 500: Ошибка сервера при получении данных
    
    **Пример ответа:**
    ```json
    {
      "status": "green",
      "statusText": "Виджет настроен",
      "name": "Питер Онлайн",
      "nickname": "@spbonline",
      "adminType": "owner",
      "membersCount": "1.2M"
    }
    ```
    """
    card = cards_db.get(nickname)
    if not card:
        raise HTTPException(status_code=404, detail="Карточка не найдена")
    return card

@router.post("/", response_model=NestedCommunityCard, status_code=status.HTTP_201_CREATED, summary="Создать NestedCommunityCard")
async def create_card(card: NestedCommunityCard):
    """
    Создает новую вложенную карточку сообщества.
    
    **Параметры:**
    - card: Данные для создания вложенной карточки (обязательно все поля)
    
    **Возвращает:**
    - Созданная вложенная карточка сообщества
    
    **Ошибки:**
    - 400: Карточка с таким nickname уже существует
    - 422: Ошибка валидации данных
    - 500: Ошибка сервера при создании
    
    **Пример запроса:**
    ```json
    {
      "status": "green",
      "statusText": "Виджет настроен",
      "name": "Новое сообщество",
      "nickname": "@newcommunity",
      "adminType": "owner",
      "membersCount": "500K"
    }
    ```
    
    **Пример ответа:**
    ```json
    {
      "status": "green",
      "statusText": "Виджет настроен",
      "name": "Новое сообщество",
      "nickname": "@newcommunity",
      "adminType": "owner",
      "membersCount": "500K"
    }
    ```
    """
    card_id = _make_id(card)
    if card_id in cards_db:
        raise HTTPException(status_code=400, detail="Карточка с таким nickname уже существует")
    cards_db[card_id] = card
    return card

@router.put("/{nickname}", response_model=NestedCommunityCard, summary="Обновить NestedCommunityCard по nickname")
async def update_card(nickname: str, card: NestedCommunityCard):
    """
    Обновляет вложенную карточку сообщества по nickname.
    
    **Параметры:**
    - nickname: Никнейм сообщества (строка, начинается с @)
    - card: Данные для обновления вложенной карточки (все поля)
    
    **Возвращает:**
    - Обновленная вложенная карточка сообщества
    
    **Ошибки:**
    - 404: Карточка не найдена
    - 422: Ошибка валидации данных
    - 500: Ошибка сервера при обновлении
    
    **Пример запроса:**
    ```json
    {
      "status": "yellow",
      "statusText": "Требуется обновление",
      "name": "Обновленное сообщество",
      "nickname": "@spbonline",
      "adminType": "admin",
      "membersCount": "1.5M"
    }
    ```
    
    **Пример ответа:**
    ```json
    {
      "status": "yellow",
      "statusText": "Требуется обновление",
      "name": "Обновленное сообщество",
      "nickname": "@spbonline",
      "adminType": "admin",
      "membersCount": "1.5M"
    }
    ```
    """
    if nickname not in cards_db:
        raise HTTPException(status_code=404, detail="Карточка не найдена")
    cards_db[nickname] = card
    return card

@router.delete("/{nickname}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить NestedCommunityCard по nickname")
async def delete_card(nickname: str):
    """
    Удаляет вложенную карточку сообщества по nickname.
    
    **Параметры:**
    - nickname: Никнейм сообщества (строка, начинается с @)
    
    **Возвращает:**
    - 204: Карточка успешно удалена
    
    **Ошибки:**
    - 404: Карточка не найдена
    - 500: Ошибка сервера при удалении
    
    **Пример использования:**
    ```
    DELETE /api/v1/nested-community-cards/@spbonline
    ```
    
    **Ответ:**
    ```
    HTTP/1.1 204 No Content
    ```
    """
    if nickname not in cards_db:
        raise HTTPException(status_code=404, detail="Карточка не найдена")
    del cards_db[nickname]
    return None 