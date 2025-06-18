# Эндпоинты для работы с розыгрышами

from fastapi import APIRouter

router = APIRouter(prefix="/raffles", tags=["Raffles"])

@router.get("/")
async def get_raffles():
    """
    Получить список розыгрышей.
    """
    return {"message": "Raffles API - в разработке"}
