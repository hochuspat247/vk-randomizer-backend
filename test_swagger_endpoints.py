#!/usr/bin/env python3
"""
Тестовый скрипт для проверки всех эндпоинтов в Swagger UI
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(url, name):
    """Тестирует эндпоинт и выводит результат"""
    try:
        response = requests.get(url, timeout=5)
        print(f"✅ {name}: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    print(f"   📊 Получено {len(data)} записей")
                elif isinstance(data, dict):
                    if 'cards' in data:
                        print(f"   📊 Получено {len(data['cards'])} карточек")
                    elif 'notifications' in data:
                        print(f"   📊 Получено {len(data['notifications'])} уведомлений")
                    elif 'modals' in data:
                        print(f"   📊 Получено {len(data['modals'])} модалок")
                    else:
                        print(f"   📊 Получен объект с ключами: {list(data.keys())}")
            except:
                print(f"   📊 Получен ответ (не JSON)")
        return True
    except Exception as e:
        print(f"❌ {name}: Ошибка - {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🧪 Тестирование эндпоинтов VK Randomizer API")
    print("=" * 50)
    
    # Тестируем корневой эндпоинт
    test_endpoint(f"{BASE_URL}/", "Корневой эндпоинт")
    
    # Тестируем эндпоинты сообществ
    print("\n🏘️  Тестирование эндпоинтов сообществ:")
    test_endpoint(f"{BASE_URL}/api/v1/communities/cards", "Список карточек сообществ")
    test_endpoint(f"{BASE_URL}/api/v1/communities/cards/1", "Карточка сообщества по ID")
    
    # Тестируем эндпоинты розыгрышей
    print("\n🎯 Тестирование эндпоинтов розыгрышей:")
    test_endpoint(f"{BASE_URL}/api/v1/raffles/", "Список розыгрышей")
    
    # Тестируем эндпоинты уведомлений
    print("\n🔔 Тестирование эндпоинтов уведомлений:")
    test_endpoint(f"{BASE_URL}/api/v1/notifications/", "Список уведомлений")
    test_endpoint(f"{BASE_URL}/api/v1/notifications/1", "Уведомление по ID")
    test_endpoint(f"{BASE_URL}/api/v1/notifications/unread/count", "Количество непрочитанных")
    
    # Тестируем эндпоинты модальных окон
    print("\n🪟 Тестирование эндпоинтов модальных окон:")
    test_endpoint(f"{BASE_URL}/api/v1/community-modals/", "Список модальных окон")
    test_endpoint(f"{BASE_URL}/api/v1/community-modals/selectMock", "Модальное окно по ID")
    
    # Тестируем эндпоинты вложенных карточек
    print("\n📋 Тестирование эндпоинтов вложенных карточек:")
    test_endpoint(f"{BASE_URL}/api/v1/nested-community-cards/", "Список вложенных карточек")
    test_endpoint(f"{BASE_URL}/api/v1/nested-community-cards/@mosnews24", "Вложенная карточка по nickname")
    
    # Тестируем эндпоинты карточек уведомлений
    print("\n📢 Тестирование эндпоинтов карточек уведомлений:")
    test_endpoint(f"{BASE_URL}/api/v1/notification-cards/", "Список карточек уведомлений")
    test_endpoint(f"{BASE_URL}/api/v1/notification-cards/38289", "Карточка уведомления по ID")
    
    print("\n" + "=" * 50)
    print("🎉 Тестирование завершено!")
    print(f"📖 Swagger UI доступен по адресу: {BASE_URL}/docs")
    print(f"📚 ReDoc доступен по адресу: {BASE_URL}/redoc")

if __name__ == "__main__":
    main() 