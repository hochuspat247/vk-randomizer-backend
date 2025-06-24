# VK Randomizer Backend

🎯 Система управления розыгрышами для VK сообществ на FastAPI

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка базы данных

Убедитесь, что PostgreSQL запущен и создайте базу данных:

```sql
CREATE DATABASE vk_randomizer;
```

### 3. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/vk_randomizer
SECRET_KEY=your-secret-key-here
```

### 4. Запуск сервера

#### 🎯 Интерактивный запуск (рекомендуется)

```bash
python run_server.py
```

Этот скрипт предоставляет:
- ✅ Проверку зависимостей
- 🔍 Проверку подключения к базе данных
- 🗄️ Интерактивную инициализацию базы данных
- 🚀 Автоматический запуск сервера

При запуске вы увидите меню:
```
🗄️  Инициализация базы данных
==================================================

Выберите действие:
1. Заполнить базу моковыми данными
2. Очистить базу данных
3. Пропустить (запустить с пустой базой)
4. Выход

Ваш выбор (1-4):
```

#### 🔧 Прямой запуск

```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 CORS Configuration

API настроен для работы с любыми доменами и поддерживает кросс-доменные запросы. 

### Доступ:
- **Любой домен** - API доступен с любого веб-сайта, включая VK Apps, локальные приложения и мобильные приложения

### Тестирование CORS:
```bash
python test_cors.py
```

Подробная документация по CORS: [docs/cors_configuration.md](docs/cors_configuration.md)

## 📚 API Документация

После запуска сервера документация доступна по адресам:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🗄️ Структура базы данных

### Communities (Сообщества)
- Полная информация о VK сообществах
- Статусы подключения и настройки
- Количество участников и розыгрышей

### Notifications (Уведомления)
- Уведомления о завершении розыгрышей
- Предупреждения и ошибки
- Информация о победителях

### Raffles (Розыгрыши)
- Детальная информация о розыгрышах
- Прогресс и время до завершения
- Статусы и настройки

## 🎯 Доступные API

### Communities
- `GET /api/v1/communities/cards` - Список всех сообществ
- `GET /api/v1/communities/cards/{id}` - Получить сообщество по ID
- `POST /api/v1/communities/cards` - Создать новое сообщество
- `PUT /api/v1/communities/cards/{id}` - Обновить сообщество
- `DELETE /api/v1/communities/cards/{id}` - Удалить сообщество

### Community Modals
- `GET /api/v1/community-modals/` - Список всех модальных окон
- `GET /api/v1/community-modals/{id}` - Получить модальное окно по ID
- `POST /api/v1/community-modals/` - Создать модальное окно
- `PUT /api/v1/community-modals/{id}` - Обновить модальное окно
- `DELETE /api/v1/community-modals/{id}` - Удалить модальное окно

### Nested Community Cards
- `GET /api/v1/nested-community-cards/` - Список вложенных карточек
- `GET /api/v1/nested-community-cards/{nickname}` - Получить по nickname
- `POST /api/v1/nested-community-cards/` - Создать карточку
- `PUT /api/v1/nested-community-cards/{nickname}` - Обновить карточку
- `DELETE /api/v1/nested-community-cards/{nickname}` - Удалить карточку

### Notifications
- `GET /api/v1/notification-cards/` - Список всех уведомлений
- `GET /api/v1/notification-cards/{id}` - Получить уведомление по ID
- `POST /api/v1/notification-cards/` - Создать уведомление
- `PUT /api/v1/notification-cards/{id}` - Обновить уведомление
- `DELETE /api/v1/notification-cards/{id}` - Удалить уведомление

### Raffles
- `GET /api/v1/raffle-cards/` - Список всех розыгрышей
- `GET /api/v1/raffle-cards/{id}` - Получить розыгрыш по ID
- `POST /api/v1/raffle-cards/` - Создать розыгрыш
- `PUT /api/v1/raffle-cards/{id}` - Обновить розыгрыш
- `DELETE /api/v1/raffle-cards/{id}` - Удалить розыгрыш

### Raffle Carousel Cards
- `GET /api/v1/raffle-carousel-cards/` - Список карточек карусели
- `GET /api/v1/raffle-carousel-cards/{id}` - Получить карточку по ID
- `POST /api/v1/raffle-carousel-cards/` - Создать карточку
- `PUT /api/v1/raffle-carousel-cards/{id}` - Обновить карточку
- `DELETE /api/v1/raffle-carousel-cards/{id}` - Удалить карточку

## 🧪 Тестирование

Запустите тесты:

```bash
pytest
```

Или используйте готовый скрипт для тестирования API:

```bash
python test_api.py
```

## 📊 Моковые данные

При выборе "Заполнить базу моковыми данными" система создаст:

### Communities
- 4 сообщества с разными статусами (green, yellow, red)
- Различные типы администраторов (owner, admin)
- Реалистичные данные участников и розыгрышей

### Notifications
- 2 завершенных розыгрыша с победителями
- 1 предупреждение о проблемах подключения
- 1 ошибка сервера

### Raffles
- 3 розыгрыша в разных режимах (both, time, members)
- Различные статусы и прогресс
- Реалистичные временные метки

## 🔧 Управление базой данных

### Инициализация
```python
from src.utils.db_init import init_database
init_database()
```

### Очистка
```python
from src.utils.db_init import clear_database
clear_database()
```

## 🛠️ Разработка

### Структура проекта
```
vk-randomizer-backend/
├── src/
│   ├── api/v1/           # API endpoints
│   ├── core/             # Конфигурация и логирование
│   ├── db/               # Модели и сессии БД
│   ├── schemas/          # Pydantic схемы
│   └── utils/            # Утилиты
├── tests/                # Тесты
├── alembic/              # Миграции БД
├── run_server.py         # Интерактивный запуск
└── requirements.txt      # Зависимости
```

### Добавление новых эндпоинтов

1. Создайте схему в `src/schemas/`
2. Создайте модель в `src/db/models/`
3. Создайте API в `src/api/v1/`
4. Добавьте роутер в `src/main.py`
5. Добавьте моковые данные в `src/utils/db_init.py`

## 📝 Логирование

Логи сохраняются в файл `logs/app.log` с уровнем INFO.

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

## 📄 Лицензия

MIT License