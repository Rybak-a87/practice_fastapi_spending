"""
рекомендуемая версия Python - 3.7
Starlet - веб сервер на основе которого все работает
	особенности:
		- легковесный ASGI фреймворк
		- один из быстрейших web-фреймворков на Python
		- WebSockets
		- GraphQL
		- фоновые задачи
pydantic - библиотека для валидации данных
	особенности:
		- валидация данных
		- сериализация - десериализация
		- управление настройками
		- одна из быстрейших библиотек в своем классе
		- основана на аннотации типов
"""
# пример работы с pydantic
from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
	id: int
	email: str
	registered_at: datetime
	last_login_at: datetime
	is_active: bool

user_data = {
	"id": 1,
	"email": "mail@mail.mail",
	"registered_at": "2021-01-01 12:00:00",
	"last_login_at": "2021-02-01 12:00:00",
	"is_active": True
}

user = User.parse_obj(user_data)    # загрузка данных в модели
print(repr(user.last_login_at))# вывод поля с датой
print(user.json())# сериализация (преобразование в json)
# пример работы с pydantic
# пример FastAPI
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/home/{name}")
def home(name: str):
	return {"message": f"Hello, {name}!"}

uvicorn.run(app)
# пример FastAPI

""" структура проекта
- файл <requeremrnts.txt> - список необходимых пакетов для проекта
- файл <.env> - хранит переменные окружения
- файл <.gitignore> - файлы и папки игнорируемые Git
- файл <README.md> - описание проекта
- все исходники в папке <src>
- внутри <src> 
	- пакет с названием проекта (пакет - директория с файлом __init__.py)
	- файл <app.py> - само приложение FastAPI
	- файл __main__.py - для запуска приложения (или команда в терминале <uvicorn app:app --reload>)
	- файл <setting.py> - хранятся настройки приложения
	- пакет <api> - хранятся обработчики API
	- пакет <views> или <services> - хранится представление (бизнес логика)
	- пакет <models> - хранит описание моделей данных (pydantic)
	- пакет <database> - хранит описание базы данных
		- файл <database.py> - код работы с базой данных (ORM и т.д.)
		- файл <tables.py> - описание таблиц базы данных (моделей)
структура проекта """
"""
# -----------------------------------------------------------------
Механизм авторизации
в качестве механизма используем jwt
# -----------------------------------------------------------------
requirements.txt
fastapi
uvicorn
pydantic
python-dotenv - для работы с dotenv файлами
sqlalchemy
python-jose - для работы с jwt
passlib[bcrypt] - для кешированияи валидации паролей
python-multipart - для использования форм
# -----------------------------------------------------------------
"""