import datetime

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.hash import bcrypt    # для валидации и хеширования паролей
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ..database import tables
from ..models.auth import UserModel, TokenModel, UserCreateModel
from ..settings import settings
from ..database.conf_db import get_session


# схема авторизации - для ограничения доступа без авторизации
cauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign-in/")    # url по которому доступна авторизация для редиректа в случае отсутствия токена


def get_current_user(token: str = Depends(cauth2_scheme)) -> UserModel:    # зависимость на схему авторизации
    """
    ограничение доступа без авторизации (как работать со схемой авторизации)
    для связи с fastapi
    читает токен из header
    валидирует токен
    возвращает пользователя
    """
    return AuthService.validate_token(token)


class AuthService:
    # утилиты для хеширования и валидации пароля
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """валидация сырого пароля и хеш пароля"""
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        """хеширование пароля"""
        return bcrypt.hash(password)
    # утилиты для хеширования и валидации пароля

    # методы для работы с JWT
    @classmethod
    def validate_token(cls, token: str) -> UserModel:
        """проверка присланного в запросе токена"""
        exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

        try:
            payload = jwt.decode(    # достаем полезную нагрузку из токена (метод jwt.decode())
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm]
            )
        except JWTError:
            raise exception from None

        user_data = payload.get("user")    # из токена достать поле user
        try:
            user = UserModel.parse_obj(user_data)    # валидирование через pydantic
        except ValidationError:
            raise exception from None
        return user

    @classmethod
    def create_token(cls, user: tables.UserDB) -> TokenModel:
        """создание токена из пользователя"""
        user_data = UserModel.from_orm(user)    # преобразование модели из orm в модель pydantic

        now_date = datetime.datetime.utcnow()
        payload = {    # формирование данных для создания токена
            "iat": now_date,    # время выпуска токена
            "nbf": now_date,    # начало действия токена
            "exp": now_date + datetime.timedelta(seconds=settings.jwt_expiration),    # время истечения действия токена
            "sub": str(user_data.id),
            "user": user_data.dict()
        }
        # формирование токена
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )

        return TokenModel(access_token=token)
    # методы для работы с JWT

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(self, user_data: UserCreateModel) -> TokenModel:    # возвращает токен так как при регистрации также происходит авторизация
        """регистрация пользователя"""
        user = tables.UserDB(
            email=user_data.email,
            username=user_data.username,
            password_hash=self.hash_password(user_data.password)
        )
        self.session.add(user)
        self.session.commit()
        return self.create_token(user)

    def authenticate_user(self, username: str, password: str) -> TokenModel:
        """авторизация пользователя"""
        exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
        user = self.session.query(tables.UserDB).filter(tables.UserDB.username == username).first()
        if not user:
            raise exception

        if not self.verify_password(password, user.password_hash):
            raise exception

        return self.create_token(user)
