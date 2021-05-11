# ---
#
# ---
import uvicorn

from .settings import settings


uvicorn.run(    # запуск приложения
    "spending.app:app",    # путь до приложения
    host=settings.server_host,    # путь к хосту из настроек
    port=settings.server_port,    # путь к порту из настроек
    reload=True    # автоматическая перезагрузка сервера
)
