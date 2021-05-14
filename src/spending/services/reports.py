import csv
from io import StringIO
from typing import Any    # любой тип

from fastapi import Depends

from ..services.operations import OperationsService
from ..models.operations import OperationCreateModel, OperationListModel


class ReportsService:
    def __init__(self, operations_service: OperationsService = Depends()):
        self.operations_service = operations_service

    def import_csv(self, user_id: int, file: Any):
        """загрузка операций из файла csv в базу данных"""
        reader = csv.DictReader(    # принимает файл и читает его в виде словарей
            (line.decode() for line in file),    # декодировка файла в байты (генератором)
            fieldnames=[    # список полей читаемые из csv
                "date",
                "kind",
                "amount",
                "description"
            ]
        )
        next(reader, None)    # пропустить шапку с заголовками
        operations = []
        for row in reader:
            operations_data = OperationCreateModel.parse_obj(row)    # преобразование в модель pydantic
            # в csv нельзя хранить значение None, следовательно преобразовываем пустую строку в None
            if operations_data.description == "":
                operations_data.description = None
            operations.append(operations_data)

        self.operations_service.create_many_operations(
            user_id=user_id,
            operations_data=operations
        )

    def export_csv(self, user_id: int, ) -> Any:
        """запись операций в файл csv из базы данных"""
        output = StringIO()    # для создания файлайк объект
        writer = csv.DictWriter(
            output,
            fieldnames=[
                "date",
                "kind",
                "amount",
                "description"
            ],
            extrasaction="ignore"    # игнорировать лишние параметры которые не указаны в fieldnames
        )
        operations = self.operations_service.get_list(user_id)

        writer.writeheader()    # записывает первую строчку, содержащую название полей
        for operation in operations:
            operation_data = OperationListModel.from_orm(operation)
            writer.writerow(operation_data.dict())

        output.seek(0)    # сбросить позицию курсора в начало
        return output
