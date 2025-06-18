#!/usr/bin/env python3
"""
Автоматический запуск VK Randomizer Backend с инициализацией БД
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Вывод баннера приложения"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    VK Randomizer Backend                     ║
║                                                              ║
║  🎯 Система управления розыгрышами для VK сообществ         ║
║  🚀 FastAPI + SQLAlchemy + PostgreSQL                       ║
║  📚 Swagger UI: http://localhost:8000/docs                  ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Проверка зависимостей"""
    print("🔍 Проверка зависимостей...")
    
    try:
        import fastapi
        import sqlalchemy
        import pydantic
        print("✅ Все зависимости установлены")
        return True
    except ImportError as e:
        print(f"❌ Отсутствует зависимость: {e}")
        print("💡 Установите зависимости: pip install -r requirements.txt")
        return False

def init_database_auto():
    """Автоматическая инициализация базы данных"""
    print("\n🗄️  Автоматическая инициализация базы данных")
    print("=" * 50)
    
    try:
        print("📊 Заполнение базы моковыми данными...")
        from src.utils.db_init import init_database
        init_database()
        print("✅ База данных успешно заполнена!")
        return True
    except Exception as e:
        print(f"❌ Ошибка при заполнении базы: {e}")
        print("⚠️  Продолжаем с пустой базой данных...")
        return True

def start_server():
    """Запуск сервера"""
    print("\n🚀 Запуск сервера...")
    print("=" * 50)
    
    # Параметры запуска
    host = "0.0.0.0"
    port = 8000
    reload = True
    
    print(f"📍 Сервер будет доступен по адресу: http://{host}:{port}")
    print(f"📚 Swagger UI: http://{host}:{port}/docs")
    print(f"🔄 Автоперезагрузка: {'Включена' if reload else 'Отключена'}")
    print("\n⏳ Запуск...")
    
    try:
        # Запуск uvicorn
        cmd = [
            sys.executable, "-m", "uvicorn",
            "src.main:app",
            "--host", host,
            "--port", str(port),
            "--reload" if reload else ""
        ]
        
        # Удаляем пустые аргументы
        cmd = [arg for arg in cmd if arg]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Сервер остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка запуска сервера: {e}")

def main():
    """Основная функция"""
    print_banner()
    
    # Проверка зависимостей
    if not check_dependencies():
        sys.exit(1)
    
    # Автоматическая инициализация базы данных
    if not init_database_auto():
        print("\n❌ Не удалось инициализировать базу данных")
        sys.exit(1)
    
    # Запуск сервера
    start_server()

if __name__ == "__main__":
    main() 