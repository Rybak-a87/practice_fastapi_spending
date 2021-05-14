# ---
# Конфигурации приложения
# ---
from pydantic import BaseSettings    # для описания настроек


class Settings(BaseSettings):
    """описания настроек"""
    server_host: str = "127.0.0.1"    # хост старта сервера
    server_port: int = 8000    # порт старта сервера
    database_url: str = "sqlite:///./db_spending.sqlite3"    # подключение к базе данных

    jwt_secret: str = ""    # секретный ключ jwt
    jwt_algorithm: str = "HS256"    # алгоритм jwt
    jwt_expiration: int = 3600    # время существования токена (в секундах)


# чтение переменных из .env файла (дотэнв файла)
settings = Settings(
    _env_file=".env",    # чтение переменных из dotenv (.env) файла - установить дополнительно пакет (<python-dotenv>)
    _env_file_encoding=" utf-8"    # кодировка dotenv (.env) файла
)
