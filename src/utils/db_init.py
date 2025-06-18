from sqlalchemy.orm import Session
from src.db.models.community import Community
from src.db.models.notification import Notification
from src.db.models.raffle import Raffle
from src.db.session import get_db
from src.schemas.community import CommunityCardCreate
from src.schemas.notification import CompletedNotificationCard, WarningNotificationCard, ErrorNotificationCard
from src.schemas.raffle import RaffleCreate
import logging

logger = logging.getLogger(__name__)

def init_community_data(db: Session):
    """Инициализация данных для сообществ"""
    communities_data = [
        {
            "id": "1",
            "name": "Техно-сообщество",
            "nickname": "@techclub",
            "membersCount": "12 500",
            "raffleCount": "8",
            "adminType": "owner",
            "avatarUrl": "https://example.com/avatar.jpg",
            "status": "green",
            "buttonDesc": "Последнее изменение: 14.10 21:31 – Администратор",
            "stateText": "Активен"
        },
        {
            "id": "2",
            "name": "Москва 24 – Новости",
            "nickname": "@mosnews24",
            "membersCount": "522K",
            "raffleCount": "15",
            "adminType": "admin",
            "avatarUrl": "https://example.com/mosnews.jpg",
            "status": "yellow",
            "buttonDesc": "Последнее изменение: 15.10 14:20 – Модератор",
            "stateText": "Требует внимания"
        },
        {
            "id": "3",
            "name": "Казань 24 – Новости",
            "nickname": "@kazan24",
            "membersCount": "804K",
            "raffleCount": "12",
            "adminType": "owner",
            "avatarUrl": "https://example.com/kazan.jpg",
            "status": "red",
            "buttonDesc": "Последнее изменение: 16.10 09:15 – Администратор",
            "stateText": "Ошибка"
        },
        {
            "id": "4",
            "name": "Санкт-Петербург Онлайн",
            "nickname": "@spbonline",
            "membersCount": "878K",
            "raffleCount": "20",
            "adminType": "admin",
            "avatarUrl": "https://example.com/spb.jpg",
            "status": "green",
            "buttonDesc": "Последнее изменение: 17.10 16:45 – Админ",
            "stateText": "Активен"
        }
    ]
    
    for data in communities_data:
        existing = db.query(Community).filter(Community.id == data["id"]).first()
        if not existing:
            community = Community(**data)
            db.add(community)
            logger.info(f"Добавлено сообщество: {data['name']}")
    
    db.commit()
    logger.info("Инициализация данных сообществ завершена")

def init_notification_data(db: Session):
    """Инициализация данных для уведомлений"""
    notifications_data = [
        {
            "id": 38289,
            "type": "completed",
            "raffleId": 38289,
            "participantsCount": 5920,
            "winners": ["593IF", "REOOJ", "DOXO"],
            "reasonEnd": "Достигнут лимит по числу участников.",
            "new": True
        },
        {
            "id": 38941,
            "type": "completed",
            "raffleId": 38941,
            "participantsCount": 4780,
            "winners": ["XZ13B", "LK9FD"],
            "reasonEnd": "Истекло время проведения розыгрыша.",
            "new": False
        },
        {
            "id": 1,
            "type": "warning",
            "warningTitle": "Не удалось подключить виджет",
            "warningDescription": [
                'Сообщество "Казань 24 – Новости"',
                'У пользователя недостаточно прав.',
                'Розыгрыш не запущен.'
            ],
            "new": True
        },
        {
            "id": 2,
            "type": "error",
            "errorTitle": "Ошибка подключения сообщества",
            "errorDescription": "На сервере VK ведутся технические работы. Приносим извинения за доставленные неудобства!",
            "new": False
        }
    ]
    
    for data in notifications_data:
        existing = db.query(Notification).filter(Notification.id == data["id"]).first()
        if not existing:
            notification = Notification(**data)
            db.add(notification)
            logger.info(f"Добавлено уведомление: {data['type']} (ID: {data['id']})")
    
    db.commit()
    logger.info("Инициализация данных уведомлений завершена")

def init_raffle_data(db: Session):
    """Инициализация данных для розыгрышей"""
    raffles_data = [
        {
            "id": "492850",
            "name": "Казань 24 – Новости",
            "textRaffleState": "Активно",
            "winnersCount": 5,
            "mode": "both",
            "memberCount": "27",
            "timeLeft": "2Д 9Ч 21М",
            "progress": 99,
            "lastModified": "14.10.2025 21:31",
            "modifiedBy": "Администратор",
            "statusСommunity": "error",
            "statusNestedCard": "green",
            "statusNestedText": "Недостаточно прав",
            "nickname": "@mosnews24",
            "membersCountNested": "522K",
            "adminType": "admin"
        },
        {
            "id": "382189",
            "name": "Москва 24 – Новости",
            "textRaffleState": "Активно",
            "winnersCount": 3,
            "mode": "time",
            "timeLeft": "1Д 2Ч",
            "progress": 72,
            "lastModified": "10.10.2025 13:10",
            "modifiedBy": "Модератор",
            "statusСommunity": "connected",
            "statusNestedCard": "yellow",
            "statusNestedText": "Требуется подтверждение",
            "nickname": "@mos24",
            "membersCountNested": "1.1M",
            "adminType": "owner"
        },
        {
            "id": "818394",
            "name": "Санкт-Петербург Онлайн",
            "textRaffleState": "Активно",
            "winnersCount": 10,
            "mode": "members",
            "memberCount": "100",
            "progress": 100,
            "lastModified": "09.10.2025 08:00",
            "modifiedBy": "Админ",
            "statusСommunity": "notConfig",
            "statusNestedCard": "red",
            "statusNestedText": "Ошибка подключения",
            "nickname": "@spbonline",
            "membersCountNested": "878K",
            "adminType": "admin"
        }
    ]
    
    for data in raffles_data:
        existing = db.query(Raffle).filter(Raffle.id == data["id"]).first()
        if not existing:
            raffle = Raffle(**data)
            db.add(raffle)
            logger.info(f"Добавлен розыгрыш: {data['name']} (ID: {data['id']})")
    
    db.commit()
    logger.info("Инициализация данных розыгрышей завершена")

def init_database():
    """Основная функция инициализации базы данных"""
    try:
        db = next(get_db())
        
        logger.info("Начинаем инициализацию базы данных...")
        
        # Инициализация данных для всех сущностей
        init_community_data(db)
        init_notification_data(db)
        init_raffle_data(db)
        
        logger.info("✅ База данных успешно инициализирована моковыми данными!")
        
    except Exception as e:
        logger.error(f"❌ Ошибка при инициализации базы данных: {e}")
        raise
    finally:
        db.close()

def clear_database():
    """Очистка базы данных"""
    try:
        db = next(get_db())
        
        logger.info("Начинаем очистку базы данных...")
        
        # Удаление всех данных
        db.query(Notification).delete()
        db.query(Raffle).delete()
        db.query(Community).delete()
        
        db.commit()
        
        logger.info("✅ База данных успешно очищена!")
        
    except Exception as e:
        logger.error(f"❌ Ошибка при очистке базы данных: {e}")
        raise
    finally:
        db.close() 