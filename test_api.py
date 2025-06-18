#!/usr/bin/env python3
"""
Тестовый скрипт для проверки CommunityCard API
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1/communities"

def test_community_api():
    print("🧪 Тестирование CommunityCard API")
    print("=" * 50)
    
    # Тестовые данные
    test_card = {
        "id": "test_1",
        "name": "Тестовое сообщество",
        "nickname": "@testcommunity",
        "membersCount": "10 000",
        "raffleCount": "5",
        "adminType": "owner",
        "avatarUrl": "https://example.com/test-avatar.jpg",
        "status": "green",
        "buttonDesc": "Тестовое описание",
        "stateText": "Активен"
    }
    
    # 1. Создание карточки
    print("1. Создание карточки сообщества...")
    try:
        response = requests.post(f"{BASE_URL}/cards", json=test_card)
        if response.status_code == 201:
            print("✅ Карточка успешно создана")
            created_card = response.json()
            print(f"   ID: {created_card['id']}")
        else:
            print(f"❌ Ошибка создания: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return
    
    # 2. Получение списка карточек
    print("\n2. Получение списка карточек...")
    try:
        response = requests.get(f"{BASE_URL}/cards")
        if response.status_code == 200:
            cards = response.json()
            print(f"✅ Получено карточек: {len(cards)}")
            for card in cards:
                print(f"   - {card['name']} (@{card['nickname']}) - {card['status']}")
        else:
            print(f"❌ Ошибка получения списка: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # 3. Получение конкретной карточки
    print(f"\n3. Получение карточки {test_card['id']}...")
    try:
        response = requests.get(f"{BASE_URL}/cards/{test_card['id']}")
        if response.status_code == 200:
            card = response.json()
            print(f"✅ Карточка найдена: {card['name']}")
        else:
            print(f"❌ Ошибка получения карточки: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # 4. Обновление карточки
    print(f"\n4. Обновление карточки {test_card['id']}...")
    update_data = {
        "name": "Обновленное тестовое сообщество",
        "membersCount": "15 000",
        "status": "yellow"
    }
    try:
        response = requests.put(f"{BASE_URL}/cards/{test_card['id']}", json=update_data)
        if response.status_code == 200:
            updated_card = response.json()
            print(f"✅ Карточка обновлена: {updated_card['name']}")
            print(f"   Новое количество участников: {updated_card['membersCount']}")
            print(f"   Новый статус: {updated_card['status']}")
        else:
            print(f"❌ Ошибка обновления: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # 5. Частичное обновление карточки
    print(f"\n5. Частичное обновление карточки {test_card['id']}...")
    patch_data = {
        "buttonDesc": "Обновленное описание кнопки",
        "raffleCount": "10"
    }
    try:
        response = requests.patch(f"{BASE_URL}/cards/{test_card['id']}", json=patch_data)
        if response.status_code == 200:
            patched_card = response.json()
            print(f"✅ Карточка частично обновлена")
            print(f"   Новое описание: {patched_card['buttonDesc']}")
            print(f"   Новое количество розыгрышей: {patched_card['raffleCount']}")
        else:
            print(f"❌ Ошибка частичного обновления: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # 6. Удаление карточки
    print(f"\n6. Удаление карточки {test_card['id']}...")
    try:
        response = requests.delete(f"{BASE_URL}/cards/{test_card['id']}")
        if response.status_code == 204:
            print("✅ Карточка успешно удалена")
        else:
            print(f"❌ Ошибка удаления: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # 7. Проверка удаления
    print(f"\n7. Проверка удаления карточки {test_card['id']}...")
    try:
        response = requests.get(f"{BASE_URL}/cards/{test_card['id']}")
        if response.status_code == 404:
            print("✅ Карточка успешно удалена (404 Not Found)")
        else:
            print(f"❌ Карточка все еще существует: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Тестирование завершено!")

if __name__ == "__main__":
    # Ждем немного, чтобы сервер успел запуститься
    print("⏳ Ожидание запуска сервера...")
    time.sleep(3)
    test_community_api() 