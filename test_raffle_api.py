#!/usr/bin/env python3
"""
Тестовый скрипт для проверки API розыгрышей
"""

import requests
import json
from datetime import datetime, timedelta

# Базовый URL API
BASE_URL = "http://localhost:8000/api/v1"

def test_create_raffle():
    """Тест создания розыгрыша"""
    print("🧪 Тестирование создания розыгрыша...")
    
    raffle_data = {
        "name": "Тестовый конкурс на лучший пост",
        "community_id": "12345",
        "contest_text": "Участвуйте в нашем тестовом конкурсе! Поделитесь своими лучшими фотографиями и выиграйте призы!",
        "photos": [
            "https://example.com/photo1.jpg",
            "https://example.com/photo2.jpg"
        ],
        "require_community_subscription": True,
        "require_telegram_subscription": True,
        "telegram_channel": "@test_channel",
        "required_communities": ["@community1", "@community2"],
        "partner_tags": ["@partner1"],
        "winners_count": 5,
        "blacklist_participants": ["@spam_user"],
        "start_date": datetime.now().isoformat(),
        "end_date": (datetime.now() + timedelta(days=30)).isoformat(),
        "max_participants": 1000,
        "publish_results": True,
        "hide_participants_count": False,
        "exclude_me": False,
        "exclude_admins": False
    }
    
    try:
        response = requests.post(f"{BASE_URL}/raffles/", json=raffle_data)
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 201:
            raffle = response.json()
            print("✅ Розыгрыш успешно создан!")
            print(f"ID: {raffle['id']}")
            print(f"Название: {raffle['name']}")
            print(f"Статус: {raffle['status']}")
            return raffle['id']
        else:
            print(f"❌ Ошибка создания розыгрыша: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")
        return None

def test_get_all_raffles_simple():
    """Тест получения всех розыгрышей без фильтров"""
    print("\n🧪 Тестирование получения всех розыгрышей (простой эндпоинт)...")
    
    try:
        response = requests.get(f"{BASE_URL}/raffles/all")
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            raffles = response.json()
            print("✅ Все розыгрыши получены!")
            print(f"Количество розыгрышей: {len(raffles)}")
            
            for raffle in raffles:
                print(f"  - {raffle['name']} (ID: {raffle['id']}, Статус: {raffle['status']})")
        else:
            print(f"❌ Ошибка получения всех розыгрышей: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")

def test_get_raffles():
    """Тест получения списка розыгрышей"""
    print("\n🧪 Тестирование получения списка розыгрышей...")
    
    try:
        response = requests.get(f"{BASE_URL}/raffles/")
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Список розыгрышей получен!")
            print(f"Всего розыгрышей: {data['total']}")
            print(f"На странице: {len(data['raffles'])}")
            
            for raffle in data['raffles']:
                print(f"  - {raffle['name']} (ID: {raffle['id']}, Статус: {raffle['status']})")
        else:
            print(f"❌ Ошибка получения списка: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")

def test_get_raffle(raffle_id):
    """Тест получения конкретного розыгрыша"""
    print(f"\n🧪 Тестирование получения розыгрыша {raffle_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/raffles/{raffle_id}")
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            raffle = response.json()
            print("✅ Розыгрыш получен!")
            print(f"Название: {raffle['name']}")
            print(f"Сообщество: {raffle['community_id']}")
            print(f"Победителей: {raffle['winners_count']}")
            print(f"Участников: {raffle['participants_count']}")
            print(f"Статус: {raffle['status']}")
        else:
            print(f"❌ Ошибка получения розыгрыша: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")

def test_update_raffle(raffle_id):
    """Тест обновления розыгрыша"""
    print(f"\n🧪 Тестирование обновления розыгрыша {raffle_id}...")
    
    update_data = {
        "name": "Обновленное название конкурса",
        "winners_count": 10,
        "max_participants": 2000
    }
    
    try:
        response = requests.put(f"{BASE_URL}/raffles/{raffle_id}", json=update_data)
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            raffle = response.json()
            print("✅ Розыгрыш успешно обновлен!")
            print(f"Новое название: {raffle['name']}")
            print(f"Новое количество победителей: {raffle['winners_count']}")
        else:
            print(f"❌ Ошибка обновления: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")

def test_change_status(raffle_id):
    """Тест изменения статуса розыгрыша"""
    print(f"\n🧪 Тестирование изменения статуса розыгрыша {raffle_id}...")
    
    try:
        response = requests.patch(f"{BASE_URL}/raffles/{raffle_id}/status?status=active")
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            raffle = response.json()
            print("✅ Статус розыгрыша изменен!")
            print(f"Новый статус: {raffle['status']}")
        else:
            print(f"❌ Ошибка изменения статуса: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")

def test_health_check():
    """Тест проверки здоровья API"""
    print("\n🧪 Тестирование проверки здоровья API...")
    
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API работает корректно!")
            print(f"Статус: {data['status']}")
        else:
            print(f"❌ Ошибка проверки здоровья: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")

def main():
    """Основная функция тестирования"""
    print("🚀 Начинаем тестирование API розыгрышей...")
    print("=" * 50)
    
    # Проверяем здоровье API
    test_health_check()
    
    # Тестируем создание розыгрыша
    raffle_id = test_create_raffle()
    
    if raffle_id:
        # Тестируем получение конкретного розыгрыша
        test_get_raffle(raffle_id)
        
        # Тестируем обновление розыгрыша
        test_update_raffle(raffle_id)
        
        # Тестируем изменение статуса
        test_change_status(raffle_id)
    
    # Тестируем получение списка розыгрышей
    test_get_raffles()
    
    # Тестируем получение всех розыгрышей (простой эндпоинт)
    test_get_all_raffles_simple()
    
    print("\n" + "=" * 50)
    print("✅ Тестирование завершено!")
    print("\n📖 Документация API доступна по адресу:")
    print("   http://localhost:8000/docs")
    print("   http://localhost:8000/redoc")

if __name__ == "__main__":
    main() 