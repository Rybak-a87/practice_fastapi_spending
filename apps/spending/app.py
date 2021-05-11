# ---

# ---
from fastapi import FastAPI

from .api import router

# создание приложения
app = FastAPI()

# подключение роутера к приложению
app.include_router(router=router)
