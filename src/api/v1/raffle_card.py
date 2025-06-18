from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
from src.schemas.raffle_card import RaffleCard, RaffleCardResponse, RaffleCardListResponse

router = APIRouter(prefix="/raffle-cards", tags=["RaffleCards"])

# In-memory demo DB
raffles_db: Dict[str, RaffleCard] = {}

# Демо-данные
raffles_db["492850"] = RaffleCard(
    raffleId="492850",
    name="Казань 24 – Новости",
    textRaffleState="Активно",
    winnersCount=5,
    mode="both",
    memberCount="27",
    timeLeft="2Д 9Ч 21М",
    progress=99,
    lastModified="14.10.2025 21:31",
    modifiedBy="Администратор",
    statusСommunity="error",
    statusNestedCard="green",
    statusNestedText="Недостаточно прав",
    nickname="@mosnews24",
    membersCountNested="522K",
    adminType="admin"
)
raffles_db["382189"] = RaffleCard(
    raffleId="382189",
    name="Москва 24 – Новости",
    textRaffleState="Активно",
    winnersCount=3,
    mode="time",
    timeLeft="1Д 2Ч",
    progress=72,
    lastModified="10.10.2025 13:10",
    modifiedBy="Модератор",
    statusСommunity="connected",
    statusNestedCard="yellow",
    statusNestedText="Требуется подтверждение",
    nickname="@mos24",
    membersCountNested="1.1M",
    adminType="owner"
)
raffles_db["818394"] = RaffleCard(
    raffleId="818394",
    name="Санкт-Петербург Онлайн",
    textRaffleState="Активно",
    winnersCount=10,
    mode="members",
    memberCount="100",
    progress=100,
    lastModified="09.10.2025 08:00",
    modifiedBy="Админ",
    statusСommunity="notConfig",
    statusNestedCard="red",
    statusNestedText="Ошибка подключения",
    nickname="@spbonline",
    membersCountNested="878K",
    adminType="admin"
)

@router.get("/", response_model=RaffleCardListResponse, summary="Получить все RaffleCard")
async def get_all_raffles():
    """
    Возвращает список всех карточек розыгрышей.
    
    **Возвращает:**
    - Список всех карточек розыгрышей с полной информацией
    
    **Примеры ответов:**
    - 200: Успешно получен список розыгрышей
    - 500: Ошибка сервера при получении данных
    
    **Пример ответа:**
    ```json
    {
      "raffles": [
        {
          "raffleId": "492850",
          "name": "Казань 24 – Новости",
          "textRaffleState": "Активно",
          "winnersCount": 5,
          "mode": "both",
          "memberCount": "27",
          "timeLeft": "2Д 9Ч 21М",
          "progress": 99,
          "lastModified": "14.10.2025 21:31",
          "modifiedBy": "Администратор",
          "statusСommunity": "error",
          "statusNestedCard": "green",
          "statusNestedText": "Недостаточно прав",
          "nickname": "@mosnews24",
          "membersCountNested": "522K",
          "adminType": "admin"
        }
      ]
    }
    ```
    """
    return {"raffles": list(raffles_db.values())}

@router.get("/{raffle_id}", response_model=RaffleCardResponse, summary="Получить RaffleCard по ID")
async def get_raffle(raffle_id: str):
    """
    Возвращает карточку розыгрыша по указанному ID.
    
    **Параметры:**
    - raffle_id: Уникальный идентификатор розыгрыша (строка)
    
    **Возвращает:**
    - Карточка розыгрыша с полной информацией
    
    **Ошибки:**
    - 404: Розыгрыш не найден
    - 500: Ошибка сервера при получении данных
    
    **Пример ответа:**
    ```json
    {
      "raffle": {
        "raffleId": "492850",
        "name": "Казань 24 – Новости",
        "textRaffleState": "Активно",
        "winnersCount": 5,
        "mode": "both",
        "memberCount": "27",
        "timeLeft": "2Д 9Ч 21М",
        "progress": 99,
        "lastModified": "14.10.2025 21:31",
        "modifiedBy": "Администратор",
        "statusСommunity": "error",
        "statusNestedCard": "green",
        "statusNestedText": "Недостаточно прав",
        "nickname": "@mosnews24",
        "membersCountNested": "522K",
        "adminType": "admin"
      }
    }
    ```
    """
    raffle = raffles_db.get(raffle_id)
    if not raffle:
        raise HTTPException(status_code=404, detail="Розыгрыш не найден")
    return {"raffle": raffle}

@router.post("/", response_model=RaffleCardResponse, status_code=status.HTTP_201_CREATED, summary="Создать RaffleCard")
async def create_raffle(raffle: RaffleCard):
    """
    Создает новую карточку розыгрыша.
    
    **Параметры:**
    - raffle: Данные для создания карточки розыгрыша (обязательно все поля)
    
    **Возвращает:**
    - Созданная карточка розыгрыша
    
    **Ошибки:**
    - 400: Розыгрыш с таким ID уже существует
    - 422: Ошибка валидации данных
    - 500: Ошибка сервера при создании
    
    **Пример запроса:**
    ```json
    {
      "raffleId": "999999",
      "name": "Новый розыгрыш",
      "textRaffleState": "Активно",
      "winnersCount": 3,
      "mode": "time",
      "timeLeft": "5Д 12Ч",
      "progress": 25,
      "lastModified": "18.06.2025 15:30",
      "modifiedBy": "Администратор",
      "statusСommunity": "connected",
      "statusNestedCard": "green",
      "statusNestedText": "Все работает",
      "nickname": "@newraffle",
      "membersCountNested": "100K",
      "adminType": "owner"
    }
    ```
    
    **Пример ответа:**
    ```json
    {
      "raffle": {
        "raffleId": "999999",
        "name": "Новый розыгрыш",
        "textRaffleState": "Активно",
        "winnersCount": 3,
        "mode": "time",
        "timeLeft": "5Д 12Ч",
        "progress": 25,
        "lastModified": "18.06.2025 15:30",
        "modifiedBy": "Администратор",
        "statusСommunity": "connected",
        "statusNestedCard": "green",
        "statusNestedText": "Все работает",
        "nickname": "@newraffle",
        "membersCountNested": "100K",
        "adminType": "owner"
      }
    }
    ```
    """
    if raffle.raffleId in raffles_db:
        raise HTTPException(status_code=400, detail="Розыгрыш с таким ID уже существует")
    raffles_db[raffle.raffleId] = raffle
    return {"raffle": raffle}

@router.put("/{raffle_id}", response_model=RaffleCardResponse, summary="Обновить RaffleCard по ID")
async def update_raffle(raffle_id: str, raffle: RaffleCard):
    """
    Обновляет карточку розыгрыша по ID.
    
    **Параметры:**
    - raffle_id: Уникальный идентификатор розыгрыша (строка)
    - raffle: Данные для обновления карточки розыгрыша (все поля)
    
    **Возвращает:**
    - Обновленная карточка розыгрыша
    
    **Ошибки:**
    - 404: Розыгрыш не найден
    - 422: Ошибка валидации данных
    - 500: Ошибка сервера при обновлении
    
    **Пример запроса:**
    ```json
    {
      "raffleId": "492850",
      "name": "Обновленное название",
      "textRaffleState": "Активно",
      "winnersCount": 7,
      "mode": "both",
      "memberCount": "50",
      "timeLeft": "1Д 5Ч",
      "progress": 85,
      "lastModified": "18.06.2025 16:00",
      "modifiedBy": "Модератор",
      "statusСommunity": "connected",
      "statusNestedCard": "yellow",
      "statusNestedText": "Обновленный статус",
      "nickname": "@mosnews24",
      "membersCountNested": "600K",
      "adminType": "admin"
    }
    ```
    
    **Пример ответа:**
    ```json
    {
      "raffle": {
        "raffleId": "492850",
        "name": "Обновленное название",
        "textRaffleState": "Активно",
        "winnersCount": 7,
        "mode": "both",
        "memberCount": "50",
        "timeLeft": "1Д 5Ч",
        "progress": 85,
        "lastModified": "18.06.2025 16:00",
        "modifiedBy": "Модератор",
        "statusСommunity": "connected",
        "statusNestedCard": "yellow",
        "statusNestedText": "Обновленный статус",
        "nickname": "@mosnews24",
        "membersCountNested": "600K",
        "adminType": "admin"
      }
    }
    ```
    """
    if raffle_id not in raffles_db:
        raise HTTPException(status_code=404, detail="Розыгрыш не найден")
    raffles_db[raffle_id] = raffle
    return {"raffle": raffle}

@router.delete("/{raffle_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить RaffleCard по ID")
async def delete_raffle(raffle_id: str):
    """
    Удаляет карточку розыгрыша по ID.
    
    **Параметры:**
    - raffle_id: Уникальный идентификатор розыгрыша (строка)
    
    **Возвращает:**
    - 204: Розыгрыш успешно удален
    
    **Ошибки:**
    - 404: Розыгрыш не найден
    - 500: Ошибка сервера при удалении
    
    **Пример использования:**
    ```
    DELETE /api/v1/raffle-cards/492850
    ```
    
    **Ответ:**
    ```
    HTTP/1.1 204 No Content
    ```
    """
    if raffle_id not in raffles_db:
        raise HTTPException(status_code=404, detail="Розыгрыш не найден")
    del raffles_db[raffle_id]
    return None 