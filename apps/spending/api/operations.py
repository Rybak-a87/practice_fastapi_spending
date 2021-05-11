# ---
# операции в приложении
# ---
from typing import List

from fastapi import APIRouter
from fastapi import Depends    # через Depends производится внедрение зависимостей


from ..database import tables
from ..database.conf_db import Session
from ..models.operations import Operation


# роутер operations
router = APIRouter(
    prefix="/operations",    # путь для обработчиков
)


# выгружать весь список операций
@router.get("/", response_model=List[Operation])    # <response_model> - указывает что возвращает роутер
def get_operations():
    session = Session()
    operations = (session.query(tables.Operation).all())    # запрос в базу данных
    session.close()
    return operations    # fastapi автоматически приобразует этот список в модели pydantic из-за response_model=
