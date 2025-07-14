from sqlalchemy import Column, String, Enum
from src.db.base import Base
import enum

class AdminType(str, enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    EDITOR = "editor"
    MODERATOR = "moderator"
    MEMBER = "member"
    ADVERTISER = "advertiser"

class Status(str, enum.Enum):
    YELLOW = "yellow"
    GREEN = "green"
    RED = "red"

class StateText(str, enum.Enum):
    ACTIVE = "Активен"
    INACTIVE = "Неактивен"
    ATTENTION = "Требует внимания"
    ERROR = "Ошибка"

class Community(Base):
    __tablename__ = "communities"

    id = Column(String, primary_key=True, index=True)
    vk_user_id = Column(String, nullable=False, index=True)  # VK user ID владельца
    name = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    membersCount = Column(String, nullable=False)
    raffleCount = Column(String, nullable=False)
    adminType = Column(Enum(AdminType), nullable=False)
    avatarUrl = Column(String, nullable=False)
    status = Column(Enum(Status), nullable=False)
    buttonDesc = Column(String, nullable=False)
    stateText = Column(Enum(StateText), nullable=False)