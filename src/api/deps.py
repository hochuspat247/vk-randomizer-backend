# Зависимости (например, подключение к БД)

from typing import Generator
from sqlalchemy.orm import Session
from src.db.session import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    Dependency для получения сессии базы данных.
    Автоматически закрывает сессию после использования.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
