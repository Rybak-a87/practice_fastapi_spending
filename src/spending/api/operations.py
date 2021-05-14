# ---
# операции в приложении
# ---
from typing import List, Optional

from fastapi import APIRouter
from fastapi import Depends    # через Depends производится внедрение зависимостей (зависимости: 1. Колабл объект - функция или просто класс. 2. Генераторы. 3. асинхронные функции и генераторы)
from fastapi import Response    # для возврата ответа
from fastapi import status

from ..models.operations import OperationListModel, OperationKindEnum, OperationCreateModel, OperationUpdateModel
from ..services.operations import OperationsService
from ..models.auth import UserModel
from ..services.auth import get_current_user

# роутер operations
router = APIRouter(
    prefix="/operations",    # путь для обработчиков
)


# выгружать весь список операций с филтрацией по типу операции
@router.get("/", response_model=List[OperationListModel])    # <response_model> - указывает что возвращает роутер
def get_operations(
    # kind: OperationKind,    # фильтр по типу орераций (обязательный)
    kind: Optional[OperationKindEnum] = None,    # фильтр по типу орераций (Optional[...] = None - не обязательный)
    user: UserModel = Depends(get_current_user),    # доступ только авторизированному пользователь
    service: OperationsService = Depends(),    # внедрение зависимостей
):
    return service.get_list(user_id=user.id, kind=kind)    # fastapi автоматически приобразует этот список в модели pydantic из-за response_model=


# создание новой операции
@router.post("/", response_model=OperationListModel)
def create_operation(
        operation_data: OperationCreateModel,
        user: UserModel = Depends(get_current_user),
        service: OperationsService = Depends(),
):
    return service.create(user_id=user.id, operation_data=operation_data)


# вывести одну операцию
@router.get("/{operation_id}", response_model=OperationListModel)
def get_operation_detail(
        operation_id: int,
        user: UserModel = Depends(get_current_user),
        service: OperationsService = Depends()
):
    return service.get_detail(user_id=user.id, operation_id=operation_id)


# изменение операции
@router.put("/{operation_id}", response_model=OperationListModel)
def update_operation(
        operation_id: int,
        operation_data: OperationUpdateModel,
        user: UserModel = Depends(get_current_user),
        service: OperationsService = Depends()
):
    return service.update(user_id=user.id, operation_id=operation_id, operation_data=operation_data)


# удаление операции
@router.delete("/{operation_id}")    # возвращает пустой ответ
def delete_operation(
        operation_id: int,
        user: UserModel = Depends(get_current_user),
        service: OperationsService = Depends()
):
    service.delete(user_id=user.id, operation_id=operation_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)    # операция удаления возвращает код 204
