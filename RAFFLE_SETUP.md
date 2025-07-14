# 🎯 Настройка новых полей розыгрышей

## 📋 Обзор изменений

Система розыгрышей была обновлена с новыми полями согласно требованиям:

### ✅ Реализованные поля

#### Основная информация
- **Название розыгрыша** * (обязательное)
- **Сообщество** * (обязательное) - выбор из списка сообществ
- **Текст конкурсного поста** * (обязательное)
- **Фото (до 5 шт)** * (обязательное) - список URL фотографий

#### Обязательные условия участия
- **Подписка на сообщество** (галочка, по умолчанию включено)
- **Подписка на Telegram-канал** (галочка)
- **Telegram-канал** (поле ввода, если включена подписка на Telegram)
- **Теги обязательных сообществ** * (обязательное) - список тегов
- **Теги партнеров** (опциональное) - список тегов

#### Основные параметры
- **Количество победителей** * (обязательное, 1-100)
- **Черный список участников** (опциональное) - список заблокированных пользователей

#### Условия завершения розыгрыша
- **Старт розыгрыша** * (обязательное) - дата и время
- **Завершение розыгрыша** * (обязательное) - дата и время
- **Максимальное количество участников** (опциональное)

#### Дополнительные настройки
- **Опубликовать пост с итогами** (галочка, по умолчанию включено)
- **Скрыть количество участников** (галочка)
- **Не учитывать в розыгрыше меня** (галочка)
- **Не учитывать в розыгрыше администрацию сообщества** (галочка)

## 🗄️ Структура базы данных

### Таблица `raffles`

```sql
CREATE TABLE raffles (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    community_id VARCHAR NOT NULL,
    contest_text TEXT NOT NULL,
    photos JSON NOT NULL,
    require_community_subscription BOOLEAN DEFAULT TRUE,
    require_telegram_subscription BOOLEAN DEFAULT FALSE,
    telegram_channel VARCHAR,
    required_communities JSON NOT NULL,
    partner_tags JSON DEFAULT '[]',
    winners_count INTEGER NOT NULL,
    blacklist_participants JSON DEFAULT '[]',
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    max_participants INTEGER,
    publish_results BOOLEAN DEFAULT TRUE,
    hide_participants_count BOOLEAN DEFAULT FALSE,
    exclude_me BOOLEAN DEFAULT FALSE,
    exclude_admins BOOLEAN DEFAULT FALSE,
    status rafflestatus DEFAULT 'draft',
    participants_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Enum `rafflestatus`
- `draft` - Черновик
- `active` - Активный
- `paused` - Приостановлен
- `completed` - Завершен
- `cancelled` - Отменен

## 🚀 Установка и настройка

### 1. Применение миграции

```bash
# Применить миграцию для создания новых таблиц
alembic upgrade head
```

### 2. Запуск сервера

```bash
# Запуск с автоматической инициализацией данных
python run_server_auto.py

# Или обычный запуск
python run_server.py
```

### 3. Инициализация тестовых данных

```python
from src.utils.db_init import init_database
init_database()
```

## 📚 API Endpoints

### Создание розыгрыша
```http
POST /api/v1/raffles/
Content-Type: application/json

{
    "name": "Конкурс на лучший пост",
    "community_id": "12345",
    "contest_text": "Участвуйте в нашем конкурсе!",
    "photos": ["https://example.com/photo1.jpg"],
    "require_community_subscription": true,
    "require_telegram_subscription": false,
    "required_communities": ["@community1", "@community2"],
    "partner_tags": ["@partner1"],
    "winners_count": 5,
    "blacklist_participants": ["@user1"],
    "start_date": "2025-07-09T14:33:00",
    "end_date": "2025-08-09T11:33:00",
    "max_participants": 1000,
    "publish_results": true,
    "hide_participants_count": false,
    "exclude_me": false,
    "exclude_admins": false
}
```

### Получение списка розыгрышей
```http
GET /api/v1/raffles/?page=1&per_page=10&status=active
```

### Получение конкретного розыгрыша
```http
GET /api/v1/raffles/{raffle_id}
```

### Обновление розыгрыша
```http
PUT /api/v1/raffles/{raffle_id}
Content-Type: application/json

{
    "name": "Обновленное название",
    "winners_count": 10
}
```

### Изменение статуса
```http
PATCH /api/v1/raffles/{raffle_id}/status?status=active
```

### Удаление розыгрыша
```http
DELETE /api/v1/raffles/{raffle_id}
```

## 🧪 Тестирование

### Запуск тестов
```bash
python test_raffle_api.py
```

### Проверка Swagger документации
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔧 Валидация данных

### Автоматическая валидация
- Количество фотографий: максимум 5
- Количество победителей: 1-100
- Дата завершения должна быть позже даты старта
- Обязательные поля проверяются автоматически

### Примеры ошибок валидации
```json
{
    "detail": [
        {
            "loc": ["body", "photos"],
            "msg": "ensure this value has at most 5 items",
            "type": "value_error.list.max_items"
        },
        {
            "loc": ["body", "end_date"],
            "msg": "Дата завершения должна быть позже даты старта",
            "type": "value_error"
        }
    ]
}
```

## 📊 Статусы розыгрышей

### Жизненный цикл розыгрыша
1. **draft** - Создан черновик
2. **active** - Розыгрыш активен и принимает участников
3. **paused** - Розыгрыш приостановлен
4. **completed** - Розыгрыш завершен, победители определены
5. **cancelled** - Розыгрыш отменен

### Правила изменения статуса
- Из `draft` можно перейти в `active` или `cancelled`
- Из `active` можно перейти в `paused`, `completed` или `cancelled`
- Из `paused` можно вернуться в `active` или перейти в `completed`/`cancelled`
- Из `completed` нельзя изменить статус
- Из `cancelled` нельзя изменить статус

## 🎨 Swagger UI

Swagger UI предоставляет интерактивную документацию с возможностью:
- Просмотра всех доступных эндпоинтов
- Тестирования API прямо из браузера
- Просмотра схем данных
- Генерации примеров запросов

### Доступные теги в Swagger:
- **Raffles** - Основные операции с розыгрышами
- **Communities** - Управление сообществами
- **Notifications** - Система уведомлений
- **RaffleCards** - Карточки розыгрышей
- **RaffleCarouselCards** - Карточки карусели

## 🔍 Мониторинг

### Health Check
```http
GET /health
```

### Логирование
Все операции логируются с уровнем INFO и выше. Ошибки логируются с уровнем ERROR.

## 📝 Примечания

1. **Безопасность**: Все входящие данные валидируются через Pydantic схемы
2. **Производительность**: Добавлены индексы для часто используемых полей
3. **Масштабируемость**: Поддержка пагинации для больших списков
4. **Гибкость**: Частичное обновление через PATCH запросы
5. **Документация**: Полная документация API через OpenAPI/Swagger

## 🆘 Поддержка

При возникновении проблем:
1. Проверьте логи сервера
2. Убедитесь, что база данных доступна
3. Проверьте корректность миграций
4. Обратитесь к документации API 