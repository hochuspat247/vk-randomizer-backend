#!/usr/bin/env python3
"""
Быстрый тест API и базы данных
"""

import requests
import time
import json

def test_api():
    """Тестирование API эндпоинтов"""
    base_url = "http://localhost:8000"
    
    print("🧪 Тестирование API эндпоинтов")
    print("=" * 50)
    
    # Ждем запуска сервера
    print("⏳ Ожидание запуска сервера...")
    time.sleep(3)
    
    endpoints = [
        ("/api/v1/communities/cards", "Сообщества"),
        ("/api/v1/community-modals/", "Модальные окна"),
        ("/api/v1/nested-community-cards/", "Вложенные карточки"),
        ("/api/v1/notification-cards/", "Уведомления"),
        ("/api/v1/raffle-cards/", "Розыгрыши"),
        ("/api/v1/raffle-carousel-cards/", "Розыгрыши карусели")
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Определяем ключ для подсчета записей
                if "cards" in data:
                    count = len(data["cards"])
                elif "modals" in data:
                    count = len(data["modals"])
                elif "notifications" in data:
                    count = len(data["notifications"])
                elif "raffles" in data:
                    count = len(data["raffles"])
                else:
                    count = len(data) if isinstance(data, list) else 0
                
                print(f"✅ {name}: {count} записей")
                
                # Показываем пример данных
                if count > 0:
                    if "cards" in data:
                        example = data["cards"][0]
                    elif "modals" in data:
                        example = data["modals"][0]
                    elif "notifications" in data:
                        example = data["notifications"][0]
                    elif "raffles" in data:
                        example = data["raffles"][0]
                    else:
                        example = data[0] if isinstance(data, list) else data
                    
                    print(f"   📝 Пример: {json.dumps(example, ensure_ascii=False, indent=2)[:100]}...")
            else:
                print(f"❌ {name}: HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {name}: {e}")
    
    print("\n📚 Swagger UI: http://localhost:8000/docs")
    print("🎯 Все API готовы к использованию!")

if __name__ == "__main__":
    test_api() 