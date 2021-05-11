# ---
# описание таблиц базы данных
# ---
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


# все таблици наследуются от базового класса
Base = declarative_base()


class Operation(Base):
    __tablename__ = "operations"    # имя таблицы
    id = sa.Column(sa.Integer, primary_key=True)
    date = sa.Column(sa.String)
    kind = sa.Column(sa.String)
    amount = sa.Column(sa.Numeric(10, 2))    # числа с фиксированной точкой (10 символов. 2 после запятой)
    description = sa.Column(sa.String, nullable=True)    # <nullable=True> - поле может быть пустым

    def __repr__(self):
        return f"{self.id}"

# создание базы данных
# from .conf_db import engine
# Base.metadata.create_all(engine)
