# CommunityCard API Guide

## Описание

API для работы с карточками сообществ (CommunityCard) предоставляет полный набор операций CRUD для управления данными сообществ.

## Доступные Endpoints

### 1. Получить список всех карточек сообществ
```
GET /api/v1/communities/cards
```

**Описание:** Возвращает список всех карточек сообществ в системе.

**Ответ:** Массив объектов CommunityCard

### 2. Получить карточку сообщества по ID
```
GET /api/v1/communities/cards/{card_id}
```

**Параметры:**
- `card_id` (string) - Уникальный идентификатор карточки

**Ответ:** Объект CommunityCard

**Ошибки:**
- `404` - Карточка не найдена

### 3. Создать новую карточку сообщества
```
POST /api/v1/communities/cards
```

**Тело запроса:**
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

**Ответ:** Созданная карточка сообщества

**Ошибки:**
- `400` - Карточка с таким ID уже существует

### 4. Обновить карточку сообщества (PUT)
```
PUT /api/v1/communities/cards/{card_id}
```

**Параметры:**
- `card_id` (string) - Уникальный идентификатор карточки

**Тело запроса:** Все поля необязательны
```json
{
    "name": "Обновленное название",
    "membersCount": "15 000",
    "status": "yellow"
}
```

**Ответ:** Обновленная карточка сообщества

**Ошибки:**
- `404` - Карточка не найдена

### 5. Частично обновить карточку сообщества (PATCH)
```
PATCH /api/v1/communities/cards/{card_id}
```

**Параметры:**
- `card_id` (string) - Уникальный идентификатор карточки

**Тело запроса:** Любые поля для обновления
```json
{
    "status": "red",
    "buttonDesc": "Новое описание"
}
```

**Ответ:** Обновленная карточка сообщества

**Ошибки:**
- `404` - Карточка не найдена

### 6. Удалить карточку сообщества
```
DELETE /api/v1/communities/cards/{card_id}
```

**Параметры:**
- `card_id` (string) - Уникальный идентификатор карточки

**Ответ:** `204 No Content`

**Ошибки:**
- `404` - Карточка не найдена

## Структура данных CommunityCard

### Поля:
- `id` (string) - Уникальный идентификатор карточки
- `name` (string) - Название сообщества
- `nickname` (string) - Никнейм сообщества (с символом @)
- `membersCount` (string) - Количество участников
- `raffleCount` (string) - Количество розыгрышей
- `adminType` (enum) - Тип администратора: "owner" или "admin"
- `avatarUrl` (string) - URL аватара сообщества
- `status` (enum) - Статус сообщества: "yellow", "green", "red"
- `buttonDesc` (string) - Описание кнопки/последние изменения
- `stateText` (enum) - Текст состояния: "Активен" или "Неактивен"

## Примеры использования

### Создание карточки
```bash
curl -X POST "http://localhost:8000/api/v1/communities/cards" \
     -H "Content-Type: application/json" \
     -d '{
       "id": "5",
       "name": "Новое сообщество",
       "nickname": "@newcommunity",
       "membersCount": "5 000",
       "raffleCount": "3",
       "adminType": "admin",
       "avatarUrl": "https://example.com/avatar5.jpg",
       "status": "green",
       "buttonDesc": "Последнее изменение: 15.10 10:00 – Администратор",
       "stateText": "Активен"
     }'
```

### Обновление карточки
```bash
curl -X PUT "http://localhost:8000/api/v1/communities/cards/1" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Обновленное название",
       "membersCount": "15 000",
       "status": "yellow"
     }'
```

### Удаление карточки
```bash
curl -X DELETE "http://localhost:8000/api/v1/communities/cards/1"
```

## Swagger документация

Полная интерактивная документация доступна по адресу:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Статусы сообществ

- **green** - Сообщество активно и работает корректно
- **yellow** - Сообщество требует внимания
- **red** - Сообщество неактивно или имеет проблемы

## Типы администраторов

- **owner** - Владелец сообщества
- **admin** - Администратор сообщества 