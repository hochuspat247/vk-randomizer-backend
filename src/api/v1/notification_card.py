from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
from src.schemas.notification_card import (
    NotificationCard, NotificationCardResponse, NotificationCardListResponse,
    CompletedNotificationCard, WarningNotificationCard, ErrorNotificationCard
)

router = APIRouter(prefix="/notification-cards", tags=["NotificationCards"])

# In-memory demo DB
notifications_db: Dict[int, NotificationCard] = {}

# Демо-данные
notifications_db[38289] = CompletedNotificationCard(
    type="completed",
    raffleId=38289,
    participantsCount=5920,
    winners=["593IF", "REOOJ", "DOXO"],
    reasonEnd="Достигнут лимит по числу участников.",
    new=True
)
notifications_db[38941] = CompletedNotificationCard(
    type="completed",
    raffleId=38941,
    participantsCount=4780,
    winners=["XZ13B", "LK9FD"],
    reasonEnd="Истекло время проведения розыгрыша.",
    new=False
)
notifications_db[1] = WarningNotificationCard(
    type="warning",
    warningTitle="Не удалось подключить виджет",
    warningDescription=[
        'Сообщество "Казань 24 – Новости"',
        'У пользователя недостаточно прав.',
        'Розыгрыш не запущен.'
    ],
    new=True
)
notifications_db[2] = ErrorNotificationCard(
    type="error",
    errorTitle="Ошибка подключения сообщества",
    errorDescription="На сервере VK ведутся технические работы. Приносим извинения за доставленные неудобства!",
    new=False
)

@router.get("/", response_model=NotificationCardListResponse, summary="Получить все NotificationCard")
async def get_all_notifications():
    """
    Возвращает список всех уведомлений.
    
    **Возвращает:**
    - Список всех уведомлений с их данными
    
    **Примеры ответов:**
    - 200: Успешно получен список уведомлений
    - 500: Ошибка сервера при получении данных
    
    **Пример ответа:**
    ```json
    {
      "notifications": [
        {
          "type": "completed",
          "raffleId": 38289,
          "participantsCount": 5920,
          "winners": ["593IF", "REOOJ", "DOXO"],
          "reasonEnd": "Достигнут лимит по числу участников.",
          "new": true
        },
        {
          "type": "warning",
          "warningTitle": "Не удалось подключить виджет",
          "warningDescription": [
            "Сообщество \"Казань 24 – Новости\"",
            "У пользователя недостаточно прав.",
            "Розыгрыш не запущен."
          ],
          "new": true
        }
      ]
    }
    ```
    """
    return {"notifications": list(notifications_db.values())}

@router.get("/{notification_id}", response_model=NotificationCardResponse, summary="Получить NotificationCard по ID")
async def get_notification(notification_id: int):
    """
    Возвращает уведомление по указанному ID.
    
    **Параметры:**
    - notification_id: Уникальный идентификатор уведомления (число)
    
    **Возвращает:**
    - Уведомление с полной информацией
    
    **Ошибки:**
    - 404: Уведомление не найдено
    - 500: Ошибка сервера при получении данных
    
    **Пример ответа (completed):**
    ```json
    {
      "notification": {
        "type": "completed",
        "raffleId": 38289,
        "participantsCount": 5920,
        "winners": ["593IF", "REOOJ", "DOXO"],
        "reasonEnd": "Достигнут лимит по числу участников.",
        "new": true
      }
    }
    ```
    
    **Пример ответа (warning):**
    ```json
    {
      "notification": {
        "type": "warning",
        "warningTitle": "Не удалось подключить виджет",
        "warningDescription": [
          "Сообщество \"Казань 24 – Новости\"",
          "У пользователя недостаточно прав.",
          "Розыгрыш не запущен."
        ],
        "new": true
      }
    }
    ```
    
    **Пример ответа (error):**
    ```json
    {
      "notification": {
        "type": "error",
        "errorTitle": "Ошибка подключения сообщества",
        "errorDescription": "На сервере VK ведутся технические работы. Приносим извинения за доставленные неудобства!",
        "new": false
      }
    }
    ```
    """
    notification = notifications_db.get(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Уведомление не найдено")
    return {"notification": notification}

@router.post("/", response_model=NotificationCardResponse, status_code=status.HTTP_201_CREATED, summary="Создать NotificationCard")
async def create_notification(notification: NotificationCard):
    """
    Создает новое уведомление.
    
    **Параметры:**
    - notification: Данные для создания уведомления (обязательно все поля)
    
    **Возвращает:**
    - Созданное уведомление
    
    **Ошибки:**
    - 400: Уведомление с таким raffleId уже существует
    - 422: Ошибка валидации данных
    - 500: Ошибка сервера при создании
    
    **Пример запроса (completed):**
    ```json
    {
      "type": "completed",
      "raffleId": 50000,
      "participantsCount": 3000,
      "winners": ["WIN1", "WIN2", "WIN3"],
      "reasonEnd": "Розыгрыш завершен по времени.",
      "new": true
    }
    ```
    
    **Пример запроса (warning):**
    ```json
    {
      "type": "warning",
      "warningTitle": "Новое предупреждение",
      "warningDescription": [
        "Сообщество \"Новое сообщество\"",
        "Проблема с подключением."
      ],
      "new": true
    }
    ```
    
    **Пример запроса (error):**
    ```json
    {
      "type": "error",
      "errorTitle": "Новая ошибка",
      "errorDescription": "Описание новой ошибки.",
      "new": false
    }
    ```
    
    **Пример ответа:**
    ```json
    {
      "notification": {
        "type": "completed",
        "raffleId": 50000,
        "participantsCount": 3000,
        "winners": ["WIN1", "WIN2", "WIN3"],
        "reasonEnd": "Розыгрыш завершен по времени.",
        "new": true
      }
    }
    ```
    """
    if hasattr(notification, "raffleId") and notification.raffleId in notifications_db:
        raise HTTPException(status_code=400, detail="Уведомление с таким raffleId уже существует")
    new_id = notification.raffleId if hasattr(notification, "raffleId") else max(notifications_db.keys(), default=100) + 1
    notifications_db[new_id] = notification
    return {"notification": notification}

@router.put("/{notification_id}", response_model=NotificationCardResponse, summary="Обновить NotificationCard по ID")
async def update_notification(notification_id: int, notification: NotificationCard):
    """
    Обновляет уведомление по ID.
    
    **Параметры:**
    - notification_id: Уникальный идентификатор уведомления (число)
    - notification: Данные для обновления уведомления (все поля)
    
    **Возвращает:**
    - Обновленное уведомление
    
    **Ошибки:**
    - 404: Уведомление не найдено
    - 422: Ошибка валидации данных
    - 500: Ошибка сервера при обновлении
    
    **Пример запроса:**
    ```json
    {
      "type": "completed",
      "raffleId": 38289,
      "participantsCount": 6000,
      "winners": ["NEW1", "NEW2", "NEW3"],
      "reasonEnd": "Обновленная причина завершения.",
      "new": false
    }
    ```
    
    **Пример ответа:**
    ```json
    {
      "notification": {
        "type": "completed",
        "raffleId": 38289,
        "participantsCount": 6000,
        "winners": ["NEW1", "NEW2", "NEW3"],
        "reasonEnd": "Обновленная причина завершения.",
        "new": false
      }
    }
    ```
    """
    if notification_id not in notifications_db:
        raise HTTPException(status_code=404, detail="Уведомление не найдено")
    notifications_db[notification_id] = notification
    return {"notification": notification}

@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить NotificationCard по ID")
async def delete_notification(notification_id: int):
    """
    Удаляет уведомление по ID.
    
    **Параметры:**
    - notification_id: Уникальный идентификатор уведомления (число)
    
    **Возвращает:**
    - 204: Уведомление успешно удалено
    
    **Ошибки:**
    - 404: Уведомление не найдено
    - 500: Ошибка сервера при удалении
    
    **Пример использования:**
    ```
    DELETE /api/v1/notification-cards/38289
    ```
    
    **Ответ:**
    ```
    HTTP/1.1 204 No Content
    ```
    """
    if notification_id not in notifications_db:
        raise HTTPException(status_code=404, detail="Уведомление не найдено")
    del notifications_db[notification_id]
    return None 