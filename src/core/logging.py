# Настройка логирования

import logging
from typing import Optional

def setup_logging(level: Optional[str] = None) -> None:
    """
    Настройка логирования для приложения.
    
    Args:
        level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    if level is None:
        level = "INFO"
    
    # Настройка базового логирования
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Настройка логгеров для внешних библиотек
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Логирование настроено с уровнем: {level}")
