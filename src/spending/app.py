# ---

# ---
from fastapi import FastAPI

from .api import router


tags_metadata = [
    {
        "name": "группа авторизации",
        "description": "описание группы авторизации",
    },
    {
        "name": "группа операции",
        "description": "описание группы операции",
    },
    {
        "name": "группа работы с файлами csv",
        "description": "описание группы работы с файлами csv",
    },
]


# создание приложения
app = FastAPI(
    title="Название",
    description="Описание",
    version="Версия приложения 1.0",
    openapi_tags=tags_metadata    # описание к группам
)

# подключение роутера к приложению
app.include_router(router=router)
