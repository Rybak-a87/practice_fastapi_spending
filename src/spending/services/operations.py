from typing import List, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import tables
from ..database.conf_db import get_session
from ..models.operations import OperationKindEnum, OperationCreateModel, OperationUpdateModel


class OperationsService:
    """представления operations"""
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_operation(self, user_id: int,  operation_id: int) -> tables.OperationDB:
        """
        возвращает операцию по id
        приватный метод для переиспользование
        """
        # --- одно и то же (1 и 2 - разный синтаксис)
        # # 1й вариант
        # operation = self.session.query(tables.OperationDB).filter_by(id=operation_id).first()
        # # 2й вариант
        operation = (
            self.session
            .query(tables.OperationDB)
            .filter_by(
                id=operation_id,
                user_id=user_id
            )
            .first()
        )
        # 3й вариант
        # operation = (
        #     self.session
        #         .query(tables.OperationDB)
        #         .get({"id": operation_id})
        # )
        # --- одно и то же
        if not operation:
            # если нет записи (операции) в базе данных - возбуждаем исключение
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,  # вывод исключения с кодом 404
                # detail={}    # подставляется в тело ответа (принимает pydantic модель или словарь)
            )

        return operation

    def get_list(self, user_id: int, kind: Optional[OperationKindEnum] = None) -> List[tables.OperationDB]:    # возвращает список операций
        """выводит список операций с применением фильтра по типу орерация"""
        query = self.session.query(tables.OperationDB).filter_by(user_id=user_id)    # базовый query

        # проверка есть ли фильтр
        if kind:
            query = query.filter_by(kind=kind)
        operations = query.all()  # запрос в базу данных
        return operations

    def get_detail(self, user_id: int,  operation_id: int) -> tables.OperationDB:    # возвращает экземпляр таблички Operations
        """вывод одной операвции"""
        return self._get_operation(user_id, operation_id)

    def create(self, user_id: int,  operation_data: OperationCreateModel) -> tables.OperationDB:    # возвращает экземпляр таблички Operations
        """создать операцию"""
        operation = tables.OperationDB(**operation_data.dict(), user_id=user_id)    # распоковываем модель pydantic приобразуя в словарь
        self.session.add(operation)    # добавление в сессию
        self.session.commit()    # сохранение в базе данных
        return operation

    def create_many_operations(self, user_id: int, operations_data: List[OperationCreateModel]) -> List[tables.OperationDB]:    # в версии python от 3.9 и выше List из typing можно заменить просто list
        """создать несколько операций сразу"""
        operations = [
            tables.OperationDB(
                **operation_data.dict(),
                user_id=user_id
            )
            for operation_data in operations_data
        ]
        self.session.add_all(operations)    # добавление в сессию список (несколько) объектов
        self.session.commit()
        return operations

    def update(self, user_id: int,  operation_id: int, operation_data: OperationUpdateModel) -> tables.OperationDB:
        """обновление-изменение операции"""
        operation = self._get_operation(user_id, operation_id)
        for field, value in operation_data:    # в pydantic все модели по умолчанию итерабельные, возвращают пары - (<название поля>, <его значение>)
            setattr(operation, field, value)    # обновляем поля через setattr
        self.session.commit()
        return operation

    def delete(self, user_id: int,  operation_id: int):
        """удаление операции"""
        operation = self._get_operation(user_id, operation_id)
        self.session.delete(operation)    # удаление из базы данных
        self.session.commit()
