from sqlalchemy import Column, Integer, String, Boolean, JSON, Enum, DateTime
from src.db.base import Base
import enum
from datetime import datetime

class NotificationType(enum.Enum):
    COMPLETED = "completed"
    WARNING = "warning"
    ERROR = "error"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(NotificationType), nullable=False)
    
    # Для completed уведомлений
    raffleId = Column(Integer, nullable=True)
    participantsCount = Column(Integer, nullable=True)
    winners = Column(JSON, nullable=True)  # Список победителей
    reasonEnd = Column(String, nullable=True)
    
    # Для warning уведомлений
    warningTitle = Column(String, nullable=True)
    warningDescription = Column(JSON, nullable=True)  # Список строк
    
    # Для error уведомлений
    errorTitle = Column(String, nullable=True)
    errorDescription = Column(String, nullable=True)
    
    # Общее поле
    new = Column(Boolean, default=True, nullable=False)

class UserNotificationSettings(Base):
    __tablename__ = "user_notification_settings"

    user_id = Column(String, primary_key=True, index=True)
    win_notify = Column(Boolean, default=True, nullable=False)
    start_notify = Column(Boolean, default=True, nullable=False)
    finish_notify = Column(Boolean, default=True, nullable=False)
    widget_notify = Column(Boolean, default=True, nullable=False)
    banner = Column(Boolean, default=True, nullable=False)
    sound = Column(Boolean, default=True, nullable=False)
    dnd_until = Column(DateTime, nullable=True)
