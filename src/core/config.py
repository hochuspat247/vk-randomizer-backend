from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://vkuser:mysecret123@localhost:5432/vk_randomizer_db2"
    APP_PORT: int = 8000
    
    # CORS settings - разрешаем доступ только с нужных доменов
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = False
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Добавляем настройки для избежания проблем с кодировкой
        case_sensitive = False

settings = Settings()
