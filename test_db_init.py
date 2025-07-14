#!/usr/bin/env python3
"""
Скрипт для тестирования инициализации базы данных
"""

import sys
import os

# Добавляем корневую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_db_init():
    """Тестирование инициализации базы данных"""
    print("🧪 Тестирование инициализации базы данных")
    print("=" * 50)
    
    try:
        from src.utils.db_init import init_database, clear_database
        
        # Очищаем базу данных
        print("🗑️  Очистка базы данных...")
        clear_database()
        
        # Инициализируем базу данных
        print("📊 Инициализация базы данных...")
        init_database()
        
        # Проверяем данные
        print("🔍 Проверка данных...")
        from src.db.session import get_db
        from src.db.models.community import Community
        from src.db.models.notification import Notification
        from src.db.models.raffle import Raffle
        
        db = next(get_db())
        
        # Проверяем сообщества
        communities = db.query(Community).all()
        print(f"✅ Сообщества: {len(communities)} записей")
        for comm in communities:
            print(f"   - {comm.name} ({comm.nickname}) - {comm.status}")
        
        # Проверяем уведомления
        notifications = db.query(Notification).all()
        print(f"✅ Уведомления: {len(notifications)} записей")
        for notif in notifications:
            print(f"   - {notif.type} (ID: {notif.id})")
        
        # Проверяем розыгрыши
        raffles = db.query(Raffle).all()
        print(f"✅ Розыгрыши: {len(raffles)} записей")
        for raffle in raffles:
            print(f"   - {raffle.name} (ID: {raffle.id}) - {raffle.textRaffleState}")
        
        db.close()
        
        print("\n🎉 Тестирование завершено успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        return False

def test_api_endpoints():
    """Тестирование API эндпоинтов"""
    print("\n🌐 Тестирование API эндпоинтов")
    print("=" * 50)
    
    try:
        import requests
        import time
        
        base_url = "http://localhost:8000"
        
        # Ждем запуска сервера
        print("⏳ Ожидание запуска сервера...")
        time.sleep(2)
        
        # Тестируем эндпоинты
        endpoints = [
            "/api/v1/communities/cards",
            "/api/v1/community-modals/",
            "/api/v1/nested-community-cards/",
            "/api/v1/notification-cards/",
            "/api/v1/raffles/",
        
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    count = len(data.get("cards", data.get("modals", data.get("notifications", data.get("raffles", [])))))
                    print(f"✅ {endpoint}: {count} записей")
                else:
                    print(f"❌ {endpoint}: HTTP {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"❌ {endpoint}: {e}")
        
        print("\n🎉 Тестирование API завершено!")
        return True
        
    except ImportError:
        print("⚠️  requests не установлен. Пропускаем тестирование API.")
        return True
    except Exception as e:
        print(f"❌ Ошибка при тестировании API: {e}")
        return False

def main():
    """Основная функция"""
    print("🚀 Тестирование VK Randomizer Backend")
    print("=" * 50)
    
    # Тестируем инициализацию БД
    if not test_db_init():
        print("❌ Тестирование инициализации БД не прошло")
        sys.exit(1)
    
    # Тестируем API (если сервер запущен)
    test_api_endpoints()
    
    print("\n📚 Документация доступна по адресу: http://localhost:8000/docs")
    print("🎯 Для запуска сервера используйте: python run_server.py")

if __name__ == "__main__":
    main() 