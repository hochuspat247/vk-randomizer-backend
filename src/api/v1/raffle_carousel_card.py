from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
from src.schemas.raffle_carousel_card import RaffleCarouselCard, RaffleCarouselCardResponse, RaffleCarouselCardListResponse

router = APIRouter(prefix="/raffle-carousel-cards", tags=["RaffleCarouselCards"])

# In-memory demo DB
carousel_raffles_db: Dict[str, RaffleCarouselCard] = {}

# Демо-данные
carousel_raffles_db["1001"] = RaffleCarouselCard(
    raffleId="1001",
    name="Москва 24 – Новости",
    status="active",
    stateText="Активно",
    members="4 280 участников",
    endDate="18.05 19:00",
    updatedAt="17.05.2025 16:42"
)
carousel_raffles_db["1002"] = RaffleCarouselCard(
    raffleId="1002",
    name="Санкт-Петербург – Актуально",
    status="pending",
    stateText="В ожидании",
    members="2 150 участников",
    endDate="20.05 12:30",
    updatedAt="18.05.2025 11:12"
)
carousel_raffles_db["1003"] = RaffleCarouselCard(
    raffleId="1003",
    name="Краснодар Онлайн",
    status="draft",
    stateText="Черновик",
    members="—",
    endDate="—",
    updatedAt="15.05.2025 10:15"
)
carousel_raffles_db["1004"] = RaffleCarouselCard(
    raffleId="1004",
    name="Казань Сегодня",
    status="results",
    stateText="Открыть итоги",
    members="3 700 участников",
    endDate="12.05 18:00",
    updatedAt="13.05.2025 09:00"
)
carousel_raffles_db["1005"] = RaffleCarouselCard(
    raffleId="1005",
    name="Нижний Новгород – Новости",
    status="deleted",
    stateText="Удалён",
    members="1 000 участников",
    endDate="05.05 14:30",
    updatedAt="06.05.2025 10:45"
)
carousel_raffles_db["1006"] = RaffleCarouselCard(
    raffleId="1006",
    name="Новосибирск PRO",
    status="resultsWhite",
    stateText="Открыть итоги",
    members="5 480 участников",
    endDate="09.05 22:15",
    updatedAt="10.05.2025 08:20"
)
carousel_raffles_db["1007"] = RaffleCarouselCard(
    raffleId="1007",
    name="Волгоград Live",
    status="completed",
    stateText="Завершён",
    members="6 000 участников",
    endDate="11.05 20:00",
    updatedAt="12.05.2025 09:30"
)

@router.get("/", response_model=RaffleCarouselCardListResponse, summary="Получить все RaffleCarouselCard")
async def get_all_carousel_raffles():
    """
    Возвращает список всех карточек розыгрышей карусели.
    
    **Возвращает:**
    - Список всех карточек розыгрышей карусели с их данными
    
    **Примеры ответов:**
    - 200: Успешно получен список розыгрышей карусели
    - 500: Ошибка сервера при получении данных
    
    **Пример ответа:**
    ```json
    {
      "raffles": [
        {
          "raffleId": "1001",
          "name": "Москва 24 – Новости",
          "status": "active",
          "stateText": "Активно",
          "members": "4 280 участников",
          "endDate": "18.05 19:00",
          "updatedAt": "17.05.2025 16:42"
        },
        {
          "raffleId": "1002",
          "name": "Санкт-Петербург – Актуально",
          "status": "pending",
          "stateText": "В ожидании",
          "members": "2 150 участников",
          "endDate": "20.05 12:30",
          "updatedAt": "18.05.2025 11:12"
        }
      ]
    }
    ```
    
    **Поддерживаемые статусы:**
    - `active` - Активно
    - `pending` - В ожидании
    - `draft` - Черновик
    - `results` - Открыть итоги
    - `deleted` - Удалён
    - `resultsWhite` - Открыть итоги (белая тема)
    - `completed` - Завершён
    """
    return {"raffles": list(carousel_raffles_db.values())}

@router.get("/{raffle_id}", response_model=RaffleCarouselCardResponse, summary="Получить RaffleCarouselCard по ID")
async def get_carousel_raffle(raffle_id: str):
    """
    Возвращает карточку розыгрыша карусели по указанному ID.
    
    **Параметры:**
    - raffle_id: Уникальный идентификатор розыгрыша карусели (строка)
    
    **Возвращает:**
    - Карточка розыгрыша карусели с полной информацией
    
    **Ошибки:**
    - 404: Розыгрыш не найден
    - 500: Ошибка сервера при получении данных
    
    **Пример ответа:**
    ```json
    {
      "raffle": {
        "raffleId": "1001",
        "name": "Москва 24 – Новости",
        "status": "active",
        "stateText": "Активно",
        "members": "4 280 участников",
        "endDate": "18.05 19:00",
        "updatedAt": "17.05.2025 16:42"
      }
    }
    ```
    """
    raffle = carousel_raffles_db.get(raffle_id)
    if not raffle:
        raise HTTPException(status_code=404, detail="Розыгрыш не найден")
    return {"raffle": raffle}

@router.post("/", response_model=RaffleCarouselCardResponse, status_code=status.HTTP_201_CREATED, summary="Создать RaffleCarouselCard")
async def create_carousel_raffle(raffle: RaffleCarouselCard):
    """
    Создает новую карточку розыгрыша карусели.
    
    **Параметры:**
    - raffle: Данные для создания карточки розыгрыша карусели (обязательно все поля)
    
    **Возвращает:**
    - Созданная карточка розыгрыша карусели
    
    **Ошибки:**
    - 400: Розыгрыш с таким ID уже существует
    - 422: Ошибка валидации данных
    - 500: Ошибка сервера при создании
    
    **Пример запроса:**
    ```json
    {
      "raffleId": "9999",
      "name": "Новый розыгрыш карусели",
      "status": "active",
      "stateText": "Активно",
      "members": "1 000 участников",
      "endDate": "25.06 15:00",
      "updatedAt": "18.06.2025 14:30"
    }
    ```
    
    **Пример ответа:**
    ```json
    {
      "raffle": {
        "raffleId": "9999",
        "name": "Новый розыгрыш карусели",
        "status": "active",
        "stateText": "Активно",
        "members": "1 000 участников",
        "endDate": "25.06 15:00",
        "updatedAt": "18.06.2025 14:30"
      }
    }
    ```
    
    **Поддерживаемые статусы:**
    - `active` - Активно
    - `pending` - В ожидании
    - `draft` - Черновик
    - `results` - Открыть итоги
    - `deleted` - Удалён
    - `resultsWhite` - Открыть итоги (белая тема)
    - `completed` - Завершён
    """
    if raffle.raffleId in carousel_raffles_db:
        raise HTTPException(status_code=400, detail="Розыгрыш с таким ID уже существует")
    carousel_raffles_db[raffle.raffleId] = raffle
    return {"raffle": raffle}

@router.put("/{raffle_id}", response_model=RaffleCarouselCardResponse, summary="Обновить RaffleCarouselCard по ID")
async def update_carousel_raffle(raffle_id: str, raffle: RaffleCarouselCard):
    """
    Обновляет карточку розыгрыша карусели по ID.
    
    **Параметры:**
    - raffle_id: Уникальный идентификатор розыгрыша карусели (строка)
    - raffle: Данные для обновления карточки розыгрыша карусели (все поля)
    
    **Возвращает:**
    - Обновленная карточка розыгрыша карусели
    
    **Ошибки:**
    - 404: Розыгрыш не найден
    - 422: Ошибка валидации данных
    - 500: Ошибка сервера при обновлении
    
    **Пример запроса:**
    ```json
    {
      "raffleId": "1001",
      "name": "Обновленное название",
      "status": "pending",
      "stateText": "В ожидании",
      "members": "5 000 участников",
      "endDate": "20.06 18:00",
      "updatedAt": "18.06.2025 15:00"
    }
    ```
    
    **Пример ответа:**
    ```json
    {
      "raffle": {
        "raffleId": "1001",
        "name": "Обновленное название",
        "status": "pending",
        "stateText": "В ожидании",
        "members": "5 000 участников",
        "endDate": "20.06 18:00",
        "updatedAt": "18.06.2025 15:00"
      }
    }
    ```
    """
    if raffle_id not in carousel_raffles_db:
        raise HTTPException(status_code=404, detail="Розыгрыш не найден")
    carousel_raffles_db[raffle_id] = raffle
    return {"raffle": raffle}

@router.delete("/{raffle_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить RaffleCarouselCard по ID")
async def delete_carousel_raffle(raffle_id: str):
    """
    Удаляет карточку розыгрыша карусели по ID.
    
    **Параметры:**
    - raffle_id: Уникальный идентификатор розыгрыша карусели (строка)
    
    **Возвращает:**
    - 204: Розыгрыш успешно удален
    
    **Ошибки:**
    - 404: Розыгрыш не найден
    - 500: Ошибка сервера при удалении
    
    **Пример использования:**
    ```
    DELETE /api/v1/raffle-carousel-cards/1001
    ```
    
    **Ответ:**
    ```
    HTTP/1.1 204 No Content
    ```
    """
    if raffle_id not in carousel_raffles_db:
        raise HTTPException(status_code=404, detail="Розыгрыш не найден")
    del carousel_raffles_db[raffle_id]
    return None 