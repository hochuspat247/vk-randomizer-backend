# VK Randomizer Backend

## Требования
- Python 3.8+
- PostgreSQL

## Установка

1. Установите PostgreSQL и создайте базу данных `vk_randomizer_db`.
   - Настройте пользователя и пароль (например, `user` и `password`).
   - Убедитесь, что PostgreSQL запущен на порту 5432 (или измените `DATABASE_URL` в `.env`).

2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows