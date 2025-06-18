from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
from src.schemas.community_modal import (
    CommunityModal, CommunityModalResponse, CommunityModalListResponse,
    SelectModal, PermissionModal, SuccessModal
)

router = APIRouter(prefix="/community-modals", tags=["CommunityModals"])

# Временное хранилище (in-memory)
modals_db: Dict[str, CommunityModal] = {}

# Примеры для демо
modals_db["selectMock"] = SelectModal(
    id="selectMock",
    type="select",
    placeholder="Выберите сообщество",
    options=["Казань 24 – Новости", "Москва Life", "Краснодар Online"]
)
modals_db["permissionMock"] = PermissionModal(
    id="permissionMock",
    type="permission",
    communityName="Казань 24 – Новости",
    communityAvatar="https://example.com/avatar.jpg",
    subscribers=[
        {"name": "Андрей", "avatar": "https://example.com/avatar.jpg"},
        {"name": "София", "avatar": "https://example.com/avatar.jpg"},
        {"name": "Мария", "avatar": ""},
        {"name": "Николай", "avatar": "https://example.com/avatar.jpg"}
    ]
)
modals_db["successMock"] = SuccessModal(
    id="successMock",
    type="success",
    communityName="Казань 24 – Новости",
    communityAvatar="https://example.com/avatar.jpg"
)

@router.get("/", response_model=CommunityModalListResponse, summary="Получить все модалки")
async def get_all_modals():
    """
    Возвращает список всех модальных окон сообществ.
    
    **Возвращает:**
    - Список всех модальных окон с их данными
    
    **Примеры ответов:**
    - 200: Успешно получен список модалок
    - 500: Ошибка сервера при получении данных
    
    **Пример ответа:**
    ```json
    {
      "modals": [
        {
          "id": "selectMock",
          "type": "select",
          "placeholder": "Выберите сообщество",
          "options": ["Казань 24 – Новости", "Москва Life", "Краснодар Online"]
        },
        {
          "id": "permissionMock",
          "type": "permission",
          "communityName": "Казань 24 – Новости",
          "communityAvatar": "https://example.com/avatar.jpg",
          "subscribers": [
            {"name": "Андрей", "avatar": "https://example.com/avatar.jpg"},
            {"name": "София", "avatar": "https://example.com/avatar.jpg"}
          ]
        }
      ]
    }
    ```
    """
    return {"modals": list(modals_db.values())}

@router.get("/{modal_id}", response_model=CommunityModalResponse, summary="Получить модалку по ID")
async def get_modal(modal_id: str):
    """
    Возвращает модальное окно по указанному ID.
    
    **Параметры:**
    - modal_id: Уникальный идентификатор модального окна (строка)
    
    **Возвращает:**
    - Модальное окно с полной информацией
    
    **Ошибки:**
    - 404: Модалка не найдена
    - 500: Ошибка сервера при получении данных
    
    **Пример ответа (select):**
    ```json
    {
      "modal": {
        "id": "selectMock",
        "type": "select",
        "placeholder": "Выберите сообщество",
        "options": ["Казань 24 – Новости", "Москва Life", "Краснодар Online"]
      }
    }
    ```
    
    **Пример ответа (permission):**
    ```json
    {
      "modal": {
        "id": "permissionMock",
        "type": "permission",
        "communityName": "Казань 24 – Новости",
        "communityAvatar": "https://example.com/avatar.jpg",
        "subscribers": [
          {"name": "Андрей", "avatar": "https://example.com/avatar.jpg"},
          {"name": "София", "avatar": "https://example.com/avatar.jpg"}
        ]
      }
    }
    ```
    """
    modal = modals_db.get(modal_id)
    if not modal:
        raise HTTPException(status_code=404, detail="Модалка не найдена")
    return {"modal": modal}

@router.post("/", response_model=CommunityModalResponse, status_code=status.HTTP_201_CREATED, summary="Создать модалку")
async def create_modal(modal: CommunityModal):
    """
    Создает новое модальное окно.
    
    **Параметры:**
    - modal: Данные для создания модального окна (обязательно все поля)
    
    **Возвращает:**
    - Созданное модальное окно
    
    **Ошибки:**
    - 400: Модалка с таким ID уже существует
    - 422: Ошибка валидации данных
    - 500: Ошибка сервера при создании
    
    **Пример запроса (select):**
    ```json
    {
      "id": "newSelect",
      "type": "select",
      "placeholder": "Выберите сообщество",
      "options": ["Новое сообщество 1", "Новое сообщество 2"]
    }
    ```
    
    **Пример запроса (permission):**
    ```json
    {
      "id": "newPermission",
      "type": "permission",
      "communityName": "Новое сообщество",
      "communityAvatar": "https://example.com/avatar.jpg",
      "subscribers": [
        {"name": "Пользователь 1", "avatar": "https://example.com/avatar1.jpg"},
        {"name": "Пользователь 2", "avatar": "https://example.com/avatar2.jpg"}
      ]
    }
    ```
    
    **Пример ответа:**
    ```json
    {
      "modal": {
        "id": "newSelect",
        "type": "select",
        "placeholder": "Выберите сообщество",
        "options": ["Новое сообщество 1", "Новое сообщество 2"]
      }
    }
    ```
    """
    if modal.id in modals_db:
        raise HTTPException(status_code=400, detail="Модалка с таким ID уже существует")
    modals_db[modal.id] = modal
    return {"modal": modal}

@router.put("/{modal_id}", response_model=CommunityModalResponse, summary="Обновить модалку по ID")
async def update_modal(modal_id: str, modal: CommunityModal):
    """
    Обновляет модальное окно по ID.
    
    **Параметры:**
    - modal_id: Уникальный идентификатор модального окна (строка)
    - modal: Данные для обновления модального окна (все поля)
    
    **Возвращает:**
    - Обновленное модальное окно
    
    **Ошибки:**
    - 404: Модалка не найдена
    - 422: Ошибка валидации данных
    - 500: Ошибка сервера при обновлении
    
    **Пример запроса:**
    ```json
    {
      "id": "selectMock",
      "type": "select",
      "placeholder": "Обновленный placeholder",
      "options": ["Обновленная опция 1", "Обновленная опция 2"]
    }
    ```
    
    **Пример ответа:**
    ```json
    {
      "modal": {
        "id": "selectMock",
        "type": "select",
        "placeholder": "Обновленный placeholder",
        "options": ["Обновленная опция 1", "Обновленная опция 2"]
      }
    }
    ```
    """
    if modal_id not in modals_db:
        raise HTTPException(status_code=404, detail="Модалка не найдена")
    modals_db[modal_id] = modal
    return {"modal": modal}

@router.patch("/{modal_id}", response_model=CommunityModalResponse, summary="Частично обновить модалку по ID")
async def patch_modal(modal_id: str, modal: CommunityModal):
    """
    Частично обновляет модальное окно по ID.
    
    **Параметры:**
    - modal_id: Уникальный идентификатор модального окна (строка)
    - modal: Данные для частичного обновления модального окна
    
    **Возвращает:**
    - Обновленное модальное окно
    
    **Ошибки:**
    - 404: Модалка не найдена
    - 422: Ошибка валидации данных
    - 500: Ошибка сервера при обновлении
    
    **Пример запроса:**
    ```json
    {
      "placeholder": "Новый placeholder",
      "options": ["Новая опция 1", "Новая опция 2"]
    }
    ```
    
    **Пример ответа:**
    ```json
    {
      "modal": {
        "id": "selectMock",
        "type": "select",
        "placeholder": "Новый placeholder",
        "options": ["Новая опция 1", "Новая опция 2"]
      }
    }
    ```
    """
    if modal_id not in modals_db:
        raise HTTPException(status_code=404, detail="Модалка не найдена")
    modals_db[modal_id] = modal
    return {"modal": modal}

@router.delete("/{modal_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить модалку по ID")
async def delete_modal(modal_id: str):
    """
    Удаляет модальное окно по ID.
    
    **Параметры:**
    - modal_id: Уникальный идентификатор модального окна (строка)
    
    **Возвращает:**
    - 204: Модалка успешно удалена
    
    **Ошибки:**
    - 404: Модалка не найдена
    - 500: Ошибка сервера при удалении
    
    **Пример использования:**
    ```
    DELETE /api/v1/community-modals/selectMock
    ```
    
    **Ответ:**
    ```
    HTTP/1.1 204 No Content
    ```
    """
    if modal_id not in modals_db:
        raise HTTPException(status_code=404, detail="Модалка не найдена")
    del modals_db[modal_id]
    return None 