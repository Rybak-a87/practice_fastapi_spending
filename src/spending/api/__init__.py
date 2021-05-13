# ---
# разделение приложения на модульные кусочки делается с помощью роутера
# ---

from fastapi import APIRouter
from .operations import router as operations_router
from .auth import router as auth_router

# корневой роутер (к нему подключаются остальные роутеры приложения)
router = APIRouter()

# подключение роутеров к корневому роутеру
router.include_router(auth_router)
router.include_router(operations_router)
