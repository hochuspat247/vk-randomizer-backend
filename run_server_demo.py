#!/usr/bin/env python3
"""
Простой сервер для демонстрации API розыгрышей без базы данных
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1.raffle_demo import router as raffle_router

# Создаем приложение
app = FastAPI(
    title="VK Randomizer Backend - Demo",
    description="Демо-версия API для управления розыгрышами",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(raffle_router)

@app.get("/", summary="Главная страница")
async def root():
    """Главная страница API"""
    return {
        "message": "VK Randomizer Backend - Demo API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", summary="Проверка здоровья")
async def health_check():
    """Проверка здоровья API"""
    return {
        "status": "healthy",
        "message": "API работает корректно"
    }

if __name__ == "__main__":
    print("🚀 Запуск демо-сервера VK Randomizer Backend...")
    print("📖 Документация будет доступна по адресу: http://localhost:8000/docs")
    print("🔗 ReDoc: http://localhost:8000/redoc")
    print("=" * 50)
    
    uvicorn.run(
        "run_server_demo:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 