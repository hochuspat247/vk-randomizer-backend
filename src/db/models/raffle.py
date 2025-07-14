from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, Enum, JSON
from sqlalchemy.sql import func
from src.db.base import Base
import enum

class RaffleStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Raffle(Base):
    __tablename__ = "raffles"

    id = Column(String, primary_key=True, index=True)
    vk_user_id = Column(String, nullable=False, index=True)  # VK user ID владельца
    
    # Основная информация
    name = Column(String, nullable=False, index=True)
    community_id = Column(String, nullable=False, index=True)
    contest_text = Column(Text, nullable=False)
    photos = Column(JSON, nullable=False)  # Список URL фотографий
    
    # Обязательные условия участия
    require_community_subscription = Column(Boolean, default=True, nullable=False)
    require_telegram_subscription = Column(Boolean, default=False, nullable=False)
    telegram_channel = Column(String, nullable=True)
    required_communities = Column(JSON, nullable=False)  # Список тегов сообществ
    partner_tags = Column(JSON, default=[], nullable=False)  # Список тегов партнеров
    
    # Основные параметры
    winners_count = Column(Integer, nullable=False)
    blacklist_participants = Column(JSON, default=[], nullable=False)  # Список заблокированных участников
    
    # Условия завершения
    start_date = Column(DateTime, nullable=False, index=True)
    end_date = Column(DateTime, nullable=False, index=True)
    max_participants = Column(Integer, nullable=True)
    
    # Дополнительные настройки
    publish_results = Column(Boolean, default=True, nullable=False)
    hide_participants_count = Column(Boolean, default=False, nullable=False)
    exclude_me = Column(Boolean, default=False, nullable=False)
    exclude_admins = Column(Boolean, default=False, nullable=False)
    
    # Статус и метаданные
    status = Column(Enum(RaffleStatus), default=RaffleStatus.DRAFT, nullable=False, index=True)
    participants_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
