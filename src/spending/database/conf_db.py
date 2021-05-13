# ---
# подключение к дб и кокнфигурация сессии (sqlalchemy)
# ---
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..settings import settings

# подклюгчение к базе данных
engine = create_engine(
    settings.database_url,    # url базы данных
    connect_args={"check_same_thread": False},    # для работы в одном потоку
)

# создание сессии базы даненых
Session = sessionmaker(
    engine,
    autocommit=False,    # коректнее делать commit "руками"
    autoflush=False    # коректнее делать flush "руками"
)

def get_session() -> Session:
    """создать и закрытие сессии"""
    session = Session()
    try:
        yield session
    finally:
        session.close()
