from notifications.endpoints import router as notifications_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(notifications_router, prefix="/notifications", tags=["Notification Engine"])