# Эндпоинты для работы с уведомлениями

from fastapi import APIRouter

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/")
async def get_notifications():
    """
    Получить список уведомлений.
    """
    return {"message": "Notifications API - в разработке"}
