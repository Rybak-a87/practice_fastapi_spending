# ---
# Работа с pydantic
# ---
from datetime import date
from decimal import Decimal
from typing import Optional
from enum import Enum

from pydantic import BaseModel


class OperationKind(str, Enum):
    """набор допустимых значений для kind"""
    # вариант - 1
    INCOME = "income"
    # вариант - 2
    OUTCOME = "outcome"


class Operation(BaseModel):
    """схема операция"""
    id: int
    date: str
    kind: OperationKind   # набор допустимых значений
    amount: Decimal
    description: Optional[str]

    class Config:
        """
        загружаем модель не из python словарей,
        а из моделей наших моделей орм
        """
        orm_mode = True
