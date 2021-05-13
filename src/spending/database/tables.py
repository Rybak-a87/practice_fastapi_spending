# ---
# описание таблиц базы данных
# ---
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


# все таблицы наследуются от базового класса
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = sa.Column(sa.Integer, primary_key=True, unique=True)
    email = sa.Column(sa.Text, unique=True)
    username = sa.Column(sa.Text, unique=True)
    password_hash = sa.Column(sa.Text)

    def __repr__(self):
        return f"{self.id}"


class Operation(Base):
    __tablename__ = "operations"    # имя таблицы
    id = sa.Column(sa.Integer, primary_key=True, unique=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("user.id"))    # внешний ключ на таблицу user
    date = sa.Column(sa.String)
    kind = sa.Column(sa.String)
    amount = sa.Column(sa.Numeric(10, 2))    # числа с фиксированной точкой (10 символов. 2 после запятой)
    description = sa.Column(sa.String, nullable=True)    # <nullable=True> - поле может быть пустым

    def __repr__(self):
        return f"{self.id}"


# создание базы данных
# from .conf_db import engine
# Base.metadata.create_all(engine)
