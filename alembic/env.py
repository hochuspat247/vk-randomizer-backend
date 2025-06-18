import os
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в sys.path
BASE_DIR = str(Path(__file__).resolve().parent.parent)
sys.path.append(BASE_DIR)

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context
from src.db.base import Base
from src.db.models.community import Community  # Импортируем модель Community

# Загрузка переменных окружения из .env
load_dotenv()

config = context.config

# Установка DATABASE_URL из .env
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError("DATABASE_URL not found in .env file")
print(f"Using DATABASE_URL: {database_url}")  # Отладочный вывод

config.set_main_option('sqlalchemy.url', database_url)

connectable = engine_from_config(
    config.get_section(config.config_ini_section),
    prefix='sqlalchemy.',
    poolclass=pool.NullPool)

try:
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata
        )

        with context.begin_transaction():
            context.run_migrations()
except Exception as e:
    print(f"Database connection error: {e}")
    raise