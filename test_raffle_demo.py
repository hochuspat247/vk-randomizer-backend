#!/usr/bin/env python3
"""
Тестирование демо-версии API розыгрышей
"""

import requests
import json
from datetime import datetime, timedelta

# Базовый URL API
BASE_URL = "http://localhost:8000"

def test_health():
    """Тестирование проверки здоровья API"""
    print("🧪 Тестирование проверки здоровья API...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Статус ответа: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ API работает корректно!")
            print(f"Статус: {data.get('status')}")
        else:
            print("❌ API не отвечает")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

def test_get_all_raffles():
    """Тестирование получения всех розыгрышей"""
    print("🧪 Тестирование получения всех розыгрышей...")
    try:
        response = requests.get(f"{BASE_URL}/raffles/all")
        print(f"Статус ответа: {response.status_code}")
        if response.status_code == 200:
            raffles = response.json()
            print(f"✅ Получено {len(raffles)} розыгрышей")
            
            # Показываем краткую информацию о каждом розыгрыше
            for i, raffle in enumerate(raffles, 1):
                print(f"  {i}. {raffle['name']} (ID: {raffle['id']})")
                print(f"     Статус: {raffle['status']}")
                print(f"     Участников: {raffle['participants_count']}")
                print(f"     Победителей: {raffle['winners_count']}")
                print()
        else:
            print(f"❌ Ошибка получения розыгрышей: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def test_get_raffle_by_id():
    """Тестирование получения розыгрыша по ID"""
    print("🧪 Тестирование получения розыгрыша по ID...")
    try:
        # Сначала получаем список всех розыгрышей
        response = requests.get(f"{BASE_URL}/raffles/all")
        if response.status_code == 200:
            raffles = response.json()
            if raffles:
                raffle_id = raffles[0]['id']
                print(f"Тестируем розыгрыш с ID: {raffle_id}")
                
                # Получаем конкретный розыгрыш
                response = requests.get(f"{BASE_URL}/raffles/{raffle_id}")
                print(f"Статус ответа: {response.status_code}")
                if response.status_code == 200:
                    raffle = response.json()
                    print("✅ Розыгрыш получен успешно!")
                    print(f"Название: {raffle['name']}")
                    print(f"Статус: {raffle['status']}")
                    print(f"Сообщество: {raffle['community_id']}")
                else:
                    print(f"❌ Ошибка получения розыгрыша: {response.text}")
            else:
                print("❌ Нет розыгрышей для тестирования")
        else:
            print("❌ Не удалось получить список розыгрышей")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def test_create_raffle():
    """Тестирование создания нового розыгрыша"""
    print("🧪 Тестирование создания нового розыгрыша...")
    
    # Данные для нового розыгрыша
    new_raffle = {
        "name": "Тестовый розыгрыш",
        "community_id": "test_community",
        "contest_text": "Это тестовый розыгрыш для проверки API",
        "photos": ["https://example.com/test1.jpg"],
        "require_community_subscription": True,
        "require_telegram_subscription": False,
        "telegram_channel": None,
        "required_communities": ["@test_community"],
        "partner_tags": [],
        "winners_count": 3,
        "blacklist_participants": [],
        "start_date": datetime.now().isoformat(),
        "end_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "max_participants": 100,
        "publish_results": True,
        "hide_participants_count": False,
        "exclude_me": False,
        "exclude_admins": False
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/raffles/",
            json=new_raffle,
            headers={"Content-Type": "application/json"}
        )
        print(f"Статус ответа: {response.status_code}")
        if response.status_code == 201:
            raffle = response.json()
            print("✅ Розыгрыш создан успешно!")
            print(f"ID: {raffle['id']}")
            print(f"Название: {raffle['name']}")
            print(f"Статус: {raffle['status']}")
            return raffle['id']
        else:
            print(f"❌ Ошибка создания розыгрыша: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def test_update_raffle(raffle_id):
    """Тестирование обновления розыгрыша"""
    if not raffle_id:
        print("❌ Нет ID розыгрыша для обновления")
        return
    
    print(f"🧪 Тестирование обновления розыгрыша {raffle_id}...")
    
    # Данные для обновления
    update_data = {
        "name": "Обновленный тестовый розыгрыш",
        "winners_count": 5
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/raffles/{raffle_id}",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Статус ответа: {response.status_code}")
        if response.status_code == 200:
            raffle = response.json()
            print("✅ Розыгрыш обновлен успешно!")
            print(f"Новое название: {raffle['name']}")
            print(f"Новое количество победителей: {raffle['winners_count']}")
        else:
            print(f"❌ Ошибка обновления розыгрыша: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def test_change_status(raffle_id):
    """Тестирование изменения статуса розыгрыша"""
    if not raffle_id:
        print("❌ Нет ID розыгрыша для изменения статуса")
        return
    
    print(f"🧪 Тестирование изменения статуса розыгрыша {raffle_id}...")
    
    try:
        response = requests.patch(
            f"{BASE_URL}/raffles/{raffle_id}/status?status=active"
        )
        print(f"Статус ответа: {response.status_code}")
        if response.status_code == 200:
            raffle = response.json()
            print("✅ Статус изменен успешно!")
            print(f"Новый статус: {raffle['status']}")
        else:
            print(f"❌ Ошибка изменения статуса: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def main():
    """Основная функция тестирования"""
    print("🚀 Начинаем тестирование демо-версии API розыгрышей...")
    print("=" * 50)
    
    # Тестируем здоровье API
    test_health()
    print()
    
    # Тестируем получение всех розыгрышей
    test_get_all_raffles()
    print()
    
    # Тестируем получение розыгрыша по ID
    test_get_raffle_by_id()
    print()
    
    # Тестируем создание розыгрыша
    raffle_id = test_create_raffle()
    print()
    
    # Тестируем обновление розыгрыша
    if raffle_id:
        test_update_raffle(raffle_id)
        print()
        
        # Тестируем изменение статуса
        test_change_status(raffle_id)
        print()
    
    print("=" * 50)
    print("✅ Тестирование завершено!")
    print()
    print("📖 Документация API доступна по адресу:")
    print("   http://localhost:8000/docs")
    print("   http://localhost:8000/redoc")

if __name__ == "__main__":
    main() 