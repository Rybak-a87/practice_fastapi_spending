# ---
# Работа с pydantic
# ---
from datetime import date
from decimal import Decimal
from typing import Optional
from enum import Enum

from pydantic import BaseModel


class OperationKindEnum(str, Enum):
    """набор допустимых значений для kind"""
    # вариант - 1
    INCOME = "income"
    # вариант - 2
    OUTCOME = "outcome"


class OperationBaseModel(BaseModel):
    """базовый класс с общими полями при создании и опображении орерации"""
    date: str
    kind: OperationKindEnum  # набор допустимых значений
    amount: Decimal
    description: Optional[str]


class OperationListModel(OperationBaseModel):
    """модель вывода списка операций (схема операция)"""
    id: int

    class Config:
        """
        загружаем модель не из python словарей,
        а из моделей наших моделей орм
        """
        orm_mode = True


class OperationCreateModel(OperationBaseModel):
    """создание операции"""
    pass    # pass так как новый полей нет, в срасненнии с OperationBase


class OperationUpdateModel(OperationBaseModel):
    """изменение операции"""
    pass
