#!/usr/bin/env python3
"""
Тест CORS конфигурации для VK Randomizer Backend
"""

import requests
import json

def test_cors_headers():
    """Тестирование CORS заголовков"""
    base_url = "http://localhost:8000"
    
    # Тестовые origins - теперь тестируем различные домены
    test_origins = [
        "https://user440084704-ekxc27na.tunnel.vk-apps.com",
        "https://vk-apps.com",
        "https://example.com",
        "https://myapp.com",
        "http://localhost:3000",
        "http://127.0.0.1:8080",
        "https://random-domain.org",
    ]
    
    print("🔍 Тестирование CORS конфигурации...")
    print("=" * 50)
    
    for origin in test_origins:
        print(f"\n📍 Тестируем origin: {origin}")
        
        try:
            # Отправляем OPTIONS запрос (preflight)
            headers = {
                "Origin": origin,
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Content-Type",
            }
            
            response = requests.options(f"{base_url}/api/v1/communities/cards", headers=headers)
            
            print(f"   Status Code: {response.status_code}")
            print(f"   Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not set')}")
            print(f"   Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods', 'Not set')}")
            print(f"   Access-Control-Allow-Headers: {response.headers.get('Access-Control-Allow-Headers', 'Not set')}")
            print(f"   Access-Control-Allow-Credentials: {response.headers.get('Access-Control-Allow-Credentials', 'Not set')}")
            
            if response.status_code == 200:
                print("   ✅ CORS настроен корректно")
            else:
                print("   ❌ CORS не настроен")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Сервер не запущен")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")

def test_actual_request():
    """Тестирование реального GET запроса"""
    base_url = "http://localhost:8000"
    origins = [
        "https://user440084704-ekxc27na.tunnel.vk-apps.com",
        "https://example.com",
        "http://localhost:3000",
    ]
    
    print(f"\n🔍 Тестирование GET запросов с различными origins")
    print("=" * 50)
    
    for origin in origins:
        print(f"\n📍 Тестируем GET с origin: {origin}")
        
        try:
            headers = {
                "Origin": origin,
                "Content-Type": "application/json",
            }
            
            response = requests.get(f"{base_url}/api/v1/communities/cards", headers=headers)
            
            print(f"   Status Code: {response.status_code}")
            print(f"   Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not set')}")
            
            if response.status_code == 200:
                print("   ✅ GET запрос успешен")
                try:
                    data = response.json()
                    print(f"   📊 Получено {len(data)} записей")
                except:
                    print("   📊 Ответ получен (не JSON)")
            else:
                print("   ❌ GET запрос неуспешен")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Сервер не запущен")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")

def test_wildcard_access():
    """Тестирование доступа с произвольного домена"""
    base_url = "http://localhost:8000"
    
    print(f"\n🔍 Тестирование доступа с произвольного домена")
    print("=" * 50)
    
    # Генерируем случайный домен
    import random
    import string
    
    random_domain = ''.join(random.choices(string.ascii_lowercase, k=10)) + '.com'
    origin = f"https://{random_domain}"
    
    print(f"📍 Тестируем случайный домен: {origin}")
    
    try:
        headers = {
            "Origin": origin,
            "Content-Type": "application/json",
        }
        
        response = requests.get(f"{base_url}/api/v1/communities/cards", headers=headers)
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not set')}")
        
        if response.status_code == 200:
            print("   ✅ Доступ с произвольного домена разрешен")
        else:
            print("   ❌ Доступ с произвольного домена заблокирован")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Сервер не запущен")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

if __name__ == "__main__":
    test_cors_headers()
    test_actual_request()
    test_wildcard_access() 