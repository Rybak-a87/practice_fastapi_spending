# ---
# операции в приложении
# ---
from typing import List, Optional

from fastapi import APIRouter
from fastapi import Depends    # через Depends производится внедрение зависимостей (зависимости: 1. Колабл объект - функция или просто класс. 2. Генераторы. 3. асинхронные функции и генераторы)

from ..models.operations import OperationList, OperationKind, OperationCreate
from ..services.operations import OperationsService


# роутер operations
router = APIRouter(
    prefix="/operations",    # путь для обработчиков
)


# выгружать весь список операций с филтрацией по типу операции
@router.get("/", response_model=List[OperationList])    # <response_model> - указывает что возвращает роутер
def get_operations(
    # kind: OperationKind,    # фильтр по типу орераций (обязательный)
    kind: Optional[OperationKind] = None,    # фильтр по типу орераций (Optional[...] = None - не обязательный)
    service: OperationsService = Depends(),    # внедрение зависимостей
):
    return service.get_list(kind=kind)    # fastapi автоматически приобразует этот список в модели pydantic из-за response_model=


# создание новой операции
@router.post("/", response_model=OperationList)
def create_operation(
        operation_date: OperationCreate,
        service: OperationsService = Depends(),
):
    return service.create(operation_date)