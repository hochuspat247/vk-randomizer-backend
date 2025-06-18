#!/usr/bin/env python3
"""
Интерактивный скрипт запуска VK Randomizer Backend
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

def check_database():
    """Проверка подключения к базе данных"""
    print("🔍 Проверка подключения к базе данных...")
    
    try:
        from src.db.session import get_db
        from src.db.base import Base
        from src.core.config import settings
        from sqlalchemy import text
        
        # Проверяем подключение
        db = next(get_db())
        db.execute(text("SELECT 1"))
        db.close()
        
        print("✅ Подключение к базе данных успешно")
        return True
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        print("💡 Убедитесь, что PostgreSQL запущен и настройки корректны")
        return False

def init_database_interactive():
    """Интерактивная инициализация базы данных"""
    print("\n🗄️  Инициализация базы данных")
    print("=" * 50)
    
    while True:
        choice = input("""
Выберите действие:
1. Заполнить базу моковыми данными
2. Очистить базу данных
3. Пропустить (запустить с пустой базой)
4. Выход

Ваш выбор (1-4): """).strip()
        
        if choice == "1":
            print("\n📊 Заполнение базы моковыми данными...")
            try:
                from src.utils.db_init import init_database
                init_database()
                print("✅ База данных успешно заполнена!")
                return True
            except Exception as e:
                print(f"❌ Ошибка при заполнении базы: {e}")
                return False
                
        elif choice == "2":
            print("\n🗑️  Очистка базы данных...")
            try:
                from src.utils.db_init import clear_database
                clear_database()
                print("✅ База данных очищена!")
                return True
            except Exception as e:
                print(f"❌ Ошибка при очистке базы: {e}")
                return False
                
        elif choice == "3":
            print("⏭️  Пропускаем инициализацию базы данных")
            return True
            
        elif choice == "4":
            print("👋 До свидания!")
            sys.exit(0)
            
        else:
            print("❌ Неверный выбор. Попробуйте снова.")

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
    
    # Проверка базы данных
    if not check_database():
        print("\n❓ Продолжить без проверки базы данных? (y/n): ", end="")
        if input().lower() != 'y':
            sys.exit(1)
    
    # Интерактивная инициализация базы данных
    if not init_database_interactive():
        print("\n❌ Не удалось инициализировать базу данных")
        sys.exit(1)
    
    # Запуск сервера
    start_server()

if __name__ == "__main__":
    main() 