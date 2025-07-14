#!/usr/bin/env python3
"""
Простой запуск сервера VK Randomizer Backend
Без инициализации базы данных
"""

import uvicorn
import sys
import os

# Добавляем путь к src в PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    VK Randomizer Backend                     ║")
    print("║                                                              ║")
    print("║  🎯 Система управления розыгрышами для VK сообществ         ║")
    print("║  🚀 FastAPI + SQLAlchemy + PostgreSQL                       ║")
    print("║  📚 Swagger UI: http://localhost:8000/docs                  ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    print("🔍 Проверка зависимостей...")
    try:
        import fastapi
        import sqlalchemy
        import psycopg2
        print("✅ Все зависимости установлены")
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("Установите зависимости: pip install -r requirements.txt")
        return
    
    print("🚀 Запуск сервера...")
    print("=" * 50)
    print("📍 Сервер будет доступен по адресу: http://0.0.0.0:8000")
    print("📚 Swagger UI: http://0.0.0.0:8000/docs")
    print("🔄 Автоперезагрузка: Включена")
    print("⏳ Запуск...")
    
    try:
        uvicorn.run(
            "src.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка запуска сервера: {e}")

if __name__ == "__main__":
    main() 