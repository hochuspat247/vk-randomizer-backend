# Эндпоинты для работы с уведомлениями

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi import Body
from typing import List, Dict
from src.schemas.notification import Notification, NotificationCreate, NotificationUpdate
from src.db.session import get_db
from src.db.models.notification import UserNotificationSettings as UserNotificationSettingsModel
from src.schemas.notification import UserNotificationSettings as UserNotificationSettingsSchema
from sqlalchemy.orm import Session

router = APIRouter(prefix="/notifications", tags=["Notifications"])
settings_router = APIRouter(prefix="/notification-settings", tags=["NotificationSettings"])

# In-memory demo DB
notifications_db: Dict[int, Notification] = {}

# Демо-данные
notifications_db[1] = Notification(
    id=1,
    type="INFO",
    title="Розыгрыш завершен",
    message="Розыгрыш 'Технические новинки' успешно завершен. Победители определены.",
    is_read=False,
    created_at="2025-01-18T10:30:00Z"
)
notifications_db[2] = Notification(
    id=2,
    type="WARNING",
    title="Низкий баланс",
    message="Баланс сообщества 'Москва 24' приближается к лимиту.",
    is_read=True,
    created_at="2025-01-18T09:15:00Z"
)
notifications_db[3] = Notification(
    id=3,
    type="ERROR",
    title="Ошибка подключения",
    message="Не удалось подключиться к VK API для сообщества 'Казань 24'.",
    is_read=False,
    created_at="2025-01-18T08:45:00Z"
)

@router.get("/", response_model=List[Notification], summary="Получить все уведомления")
async def get_notifications():
    """
    Возвращает список всех уведомлений.
    
    **Возвращает:**
    - Список всех уведомлений с полной информацией
    
    **Примеры ответов:**
    - 200: Успешно получен список уведомлений
    - 500: Ошибка сервера при получении данных
    
    **Пример ответа:**
    ```json
    [
      {
        "id": 1,
        "type": "INFO",
        "title": "Розыгрыш завершен",
        "message": "Розыгрыш 'Технические новинки' успешно завершен. Победители определены.",
        "is_read": false,
        "created_at": "2025-01-18T10:30:00Z"
      },
      {
        "id": 2,
        "type": "WARNING",
        "title": "Низкий баланс",
        "message": "Баланс сообщества 'Москва 24' приближается к лимиту.",
        "is_read": true,
        "created_at": "2025-01-18T09:15:00Z"
      }
    ]
    ```
    """
    return list(notifications_db.values())

@router.get("/{notification_id}", response_model=Notification, summary="Получить уведомление по ID")
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
    
    **Пример ответа:**
    ```json
    {
      "id": 1,
      "type": "INFO",
      "title": "Розыгрыш завершен",
      "message": "Розыгрыш 'Технические новинки' успешно завершен. Победители определены.",
      "is_read": false,
      "created_at": "2025-01-18T10:30:00Z"
    }
    ```
    """
    notification = notifications_db.get(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Уведомление не найдено")
    return notification

@router.post("/", response_model=Notification, status_code=status.HTTP_201_CREATED, summary="Создать уведомление")
async def create_notification(notification: NotificationCreate):
    """
    Создает новое уведомление.
    
    **Параметры:**
    - notification: Данные для создания уведомления (обязательно все поля)
    
    **Возвращает:**
    - Созданное уведомление
    
    **Ошибки:**
    - 400: Уведомление с таким ID уже существует
    - 422: Ошибка валидации данных
    - 500: Ошибка сервера при создании
    
    **Пример запроса:**
    ```json
    {
      "id": 4,
      "type": "INFO",
      "title": "Новое уведомление",
      "message": "Описание нового уведомления.",
      "is_read": false,
      "created_at": "2025-01-18T11:00:00Z"
    }
    ```
    
    **Пример ответа:**
    ```json
    {
      "id": 4,
      "type": "INFO",
      "title": "Новое уведомление",
      "message": "Описание нового уведомления.",
      "is_read": false,
      "created_at": "2025-01-18T11:00:00Z"
    }
    ```
    """
    if notification.id in notifications_db:
        raise HTTPException(status_code=400, detail="Уведомление с таким ID уже существует")
    notifications_db[notification.id] = Notification(**notification.dict())
    return notifications_db[notification.id]

@router.put("/{notification_id}", response_model=Notification, summary="Обновить уведомление")
async def update_notification(notification_id: int, notification: NotificationUpdate):
    """
    Обновляет уведомление по ID.
    
    **Параметры:**
    - notification_id: Уникальный идентификатор уведомления (число)
    - notification: Данные для обновления уведомления (все поля необязательны)
    
    **Возвращает:**
    - Обновленное уведомление
    
    **Ошибки:**
    - 404: Уведомление не найдено
    - 422: Ошибка валидации данных
    - 500: Ошибка сервера при обновлении
    
    **Пример запроса:**
    ```json
    {
      "type": "WARNING",
      "title": "Обновленное уведомление",
      "message": "Обновленное описание уведомления.",
      "is_read": true
    }
    ```
    
    **Пример ответа:**
    ```json
    {
      "id": 1,
      "type": "WARNING",
      "title": "Обновленное уведомление",
      "message": "Обновленное описание уведомления.",
      "is_read": true,
      "created_at": "2025-01-18T10:30:00Z"
    }
    ```
    """
    if notification_id not in notifications_db:
        raise HTTPException(status_code=404, detail="Уведомление не найдено")
    
    existing = notifications_db[notification_id]
    update_data = notification.dict(exclude_unset=True)
    updated_notification = existing.copy(update=update_data)
    notifications_db[notification_id] = updated_notification
    return updated_notification

@router.patch("/{notification_id}", response_model=Notification, summary="Частично обновить уведомление")
async def patch_notification(notification_id: int, notification: NotificationUpdate):
    """
    Частично обновляет уведомление по ID.
    
    **Параметры:**
    - notification_id: Уникальный идентификатор уведомления (число)
    - notification: Данные для частичного обновления уведомления (все поля необязательны)
    
    **Возвращает:**
    - Частично обновленное уведомление
    
    **Ошибки:**
    - 404: Уведомление не найдено
    - 422: Ошибка валидации данных
    - 500: Ошибка сервера при обновлении
    
    **Пример запроса:**
    ```json
    {
      "is_read": true
    }
    ```
    
    **Пример ответа:**
    ```json
    {
      "id": 1,
      "type": "INFO",
      "title": "Розыгрыш завершен",
      "message": "Розыгрыш 'Технические новинки' успешно завершен. Победители определены.",
      "is_read": true,
      "created_at": "2025-01-18T10:30:00Z"
    }
    ```
    """
    if notification_id not in notifications_db:
        raise HTTPException(status_code=404, detail="Уведомление не найдено")
    
    existing = notifications_db[notification_id]
    update_data = notification.dict(exclude_unset=True)
    updated_notification = existing.copy(update=update_data)
    notifications_db[notification_id] = updated_notification
    return updated_notification

@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить уведомление")
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
    """
    if notification_id not in notifications_db:
        raise HTTPException(status_code=404, detail="Уведомление не найдено")
    
    del notifications_db[notification_id]
    return None

@router.get("/unread/count", summary="Получить количество непрочитанных уведомлений")
async def get_unread_count():
    """
    Возвращает количество непрочитанных уведомлений.
    
    **Возвращает:**
    - Количество непрочитанных уведомлений
    
    **Пример ответа:**
    ```json
    {
      "unread_count": 2
    }
    ```
    """
    unread_count = sum(1 for notification in notifications_db.values() if not notification.is_read)
    return {"unread_count": unread_count}

@router.post("/{notification_id}/mark-read", response_model=Notification, summary="Отметить уведомление как прочитанное")
async def mark_notification_read(notification_id: int):
    """
    Отмечает уведомление как прочитанное.
    
    **Параметры:**
    - notification_id: Уникальный идентификатор уведомления (число)
    
    **Возвращает:**
    - Обновленное уведомление с is_read = true
    
    **Ошибки:**
    - 404: Уведомление не найдено
    - 500: Ошибка сервера при обновлении
    
    **Пример ответа:**
    ```json
    {
      "id": 1,
      "type": "INFO",
      "title": "Розыгрыш завершен",
      "message": "Розыгрыш 'Технические новинки' успешно завершен. Победители определены.",
      "is_read": true,
      "created_at": "2025-01-18T10:30:00Z"
    }
    ```
    """
    if notification_id not in notifications_db:
        raise HTTPException(status_code=404, detail="Уведомление не найдено")
    
    notification = notifications_db[notification_id]
    notification.is_read = True
    notifications_db[notification_id] = notification
    return notification

@settings_router.get("/{user_id}", response_model=UserNotificationSettingsSchema, summary="Получить настройки уведомлений пользователя", description="Возвращает все настройки уведомлений для указанного пользователя по его user_id. Если пользователь не найден, возвращаются значения по умолчанию.")
async def get_user_notification_settings(user_id: str, db: Session = Depends(get_db)):
    """
    Получить все настройки уведомлений пользователя по его user_id.
    Если пользователь не найден, возвращаются значения по умолчанию.
    
    **Параметры:**
    - user_id: VK user ID пользователя
    
    **Ответ:**
    - win_notify: bool — Оповещение о победе в розыгрыше
    - start_notify: bool — Оповещение о старте розыгрыша
    - finish_notify: bool — Оповещение о завершении розыгрыша
    - widget_notify: bool — Оповещение о сбоях виджета
    - banner: bool — Показывать баннеры
    - sound: bool — Включить звук и вибрацию
    - dnd_until: datetime/null — Не беспокоить до (если задано)
    """
    settings = db.query(UserNotificationSettingsModel).filter_by(user_id=user_id).first()
    if not settings:
        return UserNotificationSettingsSchema()
    return UserNotificationSettingsSchema.from_orm(settings)

@settings_router.put("/{user_id}", response_model=UserNotificationSettingsSchema, summary="Обновить все настройки уведомлений пользователя", description="Полностью обновляет все настройки уведомлений пользователя по его user_id. Все поля обязательны.")
async def update_user_notification_settings(user_id: str, new_settings: UserNotificationSettingsSchema, db: Session = Depends(get_db)):
    """
    Полностью обновить все настройки уведомлений пользователя по его user_id.
    Все поля обязательны, старые значения будут перезаписаны.
    
    **Параметры:**
    - user_id: VK user ID пользователя
    - Тело запроса: UserNotificationSettings (все поля)
    
    **Ответ:**
    - Актуальные настройки пользователя
    """
    settings = db.query(UserNotificationSettingsModel).filter_by(user_id=user_id).first()
    if not settings:
        settings = UserNotificationSettingsModel(user_id=user_id, **new_settings.dict())
        db.add(settings)
    else:
        for field, value in new_settings.dict().items():
            setattr(settings, field, value)
    db.commit()
    db.refresh(settings)
    return UserNotificationSettingsSchema.from_orm(settings)

@settings_router.patch("/{user_id}", response_model=UserNotificationSettingsSchema, summary="Частично обновить настройки уведомлений пользователя", description="Частично обновляет настройки уведомлений пользователя по его user_id. Можно передавать только изменяемые поля.")
async def patch_user_notification_settings(user_id: str, patch: dict = Body(...), db: Session = Depends(get_db)):
    """
    Частично обновить настройки уведомлений пользователя по его user_id.
    Можно передавать только те поля, которые нужно изменить.
    
    **Параметры:**
    - user_id: VK user ID пользователя
    - Тело запроса: dict (любые из полей настроек)
    
    **Ответ:**
    - Актуальные настройки пользователя
    """
    settings = db.query(UserNotificationSettingsModel).filter_by(user_id=user_id).first()
    if not settings:
        settings = UserNotificationSettingsModel(user_id=user_id)
        db.add(settings)
    for field, value in patch.items():
        if hasattr(settings, field):
            setattr(settings, field, value)
    db.commit()
    db.refresh(settings)
    return UserNotificationSettingsSchema.from_orm(settings)
