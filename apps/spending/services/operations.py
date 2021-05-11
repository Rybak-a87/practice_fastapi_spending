from typing import List, Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from ..database import tables
from ..database.conf_db import get_session
from ..models.operations import OperationKind, OperationCreate


class OperationsService:
    """представления operations"""
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list(self, kind: Optional[OperationKind] = None) -> List[tables.Operation]:    # возвращает список операций
        """выводит список операций с применением фильтра по типу орерация"""
        query = self.session.query(tables.Operation)    # базовый query

        # проверка есть ли фильтр
        if kind:
            query = query.filter_by(kind=kind)
        operations = query.all()  # запрос в базу данных
        return operations

    def create(self, operation_date: OperationCreate) -> tables.Operation:    # возвращает экземпляр таблички Operations
        """создать операцию"""
        operation = tables.Operation(**operation_date.dict())    # распоковываем модель pydantic приобразуя в словарь
        self.session.add(operation)    # добавление в сессию
        self.session.commit()    # сохранение в базе данных
        return operation
