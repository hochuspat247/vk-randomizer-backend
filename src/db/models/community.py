from sqlalchemy import Column, String, Enum
from src.db.base import Base
import enum

class AdminType(str, enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"

class Status(str, enum.Enum):
    YELLOW = "yellow"
    GREEN = "green"
    RED = "red"

class StateText(str, enum.Enum):
    ACTIVE = "Активен"
    INACTIVE = "Неактивен"

class Community(Base):
    __tablename__ = "communities"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    membersCount = Column(String, nullable=False)
    raffleCount = Column(String, nullable=False)
    adminType = Column(Enum(AdminType), nullable=False)
    avatarUrl = Column(String, nullable=False)
    status = Column(Enum(Status), nullable=False)
    buttonDesc = Column(String, nullable=False)
    stateText = Column(Enum(StateText), nullable=False)