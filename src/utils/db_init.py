from sqlalchemy.orm import Session
from src.db.models.community import Community
from src.db.models.notification import Notification, NotificationType
from src.db.models.raffle import Raffle, RaffleStatus
from src.db.session import get_db
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
            "stateText": "ACTIVE"
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
            "stateText": "ATTENTION"
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
            "stateText": "ERROR"
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
            "stateText": "ACTIVE"
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
            "type": NotificationType.COMPLETED,
            "raffleId": 38289,
            "participantsCount": 5920,
            "winners": ["593IF", "REOOJ", "DOXO"],
            "reasonEnd": "Достигнут лимит по числу участников.",
            "new": True
        },
        {
            "id": 38941,
            "type": NotificationType.COMPLETED,
            "raffleId": 38941,
            "participantsCount": 4780,
            "winners": ["XZ13B", "LK9FD"],
            "reasonEnd": "Истекло время проведения розыгрыша.",
            "new": False
        },
        {
            "id": 1,
            "type": NotificationType.WARNING,
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
            "type": NotificationType.ERROR,
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
    from datetime import datetime, timedelta
    
    raffles_data = [
        {
            "id": "492850",
            "name": "Конкурс на лучший пост о лете",
            "community_id": "1",
            "contest_text": "Поделитесь своими лучшими летними фотографиями и выиграйте призы! Условия участия: подписка на сообщество и лайк поста.",
            "photos": ["https://example.com/summer1.jpg", "https://example.com/summer2.jpg"],
            "require_community_subscription": True,
            "require_telegram_subscription": False,
            "telegram_channel": None,
            "required_communities": ["@techclub", "@mosnews24"],
            "partner_tags": ["@summer_partner"],
            "winners_count": 5,
            "blacklist_participants": ["@spam_user"],
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=30),
            "max_participants": 1000,
            "publish_results": True,
            "hide_participants_count": False,
            "exclude_me": False,
            "exclude_admins": False,
            "status": RaffleStatus.ACTIVE,
            "participants_count": 127
        },
        {
            "id": "382189",
            "name": "Розыгрыш подарков к Новому году",
            "community_id": "2",
            "contest_text": "Новогодний розыгрыш! Подпишитесь на наш Telegram-канал и участвуйте в розыгрыше призов.",
            "photos": ["https://example.com/newyear1.jpg"],
            "require_community_subscription": True,
            "require_telegram_subscription": True,
            "telegram_channel": "@newyear_channel",
            "required_communities": ["@mosnews24"],
            "partner_tags": ["@gift_partner", "@holiday_partner"],
            "winners_count": 3,
            "blacklist_participants": [],
            "start_date": datetime.now() - timedelta(days=5),
            "end_date": datetime.now() + timedelta(days=25),
            "max_participants": 500,
            "publish_results": True,
            "hide_participants_count": True,
            "exclude_me": True,
            "exclude_admins": True,
            "status": RaffleStatus.ACTIVE,
            "participants_count": 89
        },
        {
            "id": "818394",
            "name": "Конкурс репостов",
            "community_id": "3",
            "contest_text": "Сделайте репост этого поста и участвуйте в розыгрыше! Простые условия участия.",
            "photos": ["https://example.com/repost1.jpg", "https://example.com/repost2.jpg", "https://example.com/repost3.jpg"],
            "require_community_subscription": True,
            "require_telegram_subscription": False,
            "telegram_channel": None,
            "required_communities": ["@kazan24"],
            "partner_tags": [],
            "winners_count": 10,
            "blacklist_participants": ["@bot1", "@bot2"],
            "start_date": datetime.now() - timedelta(days=10),
            "end_date": datetime.now() + timedelta(days=20),
            "max_participants": None,
            "publish_results": False,
            "hide_participants_count": False,
            "exclude_me": False,
            "exclude_admins": False,
            "status": RaffleStatus.DRAFT,
            "participants_count": 0
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