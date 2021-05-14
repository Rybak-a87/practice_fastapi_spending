from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm    # для авторизации

from ..models.auth import UserCreateModel, TokenModel, UserModel
from ..services.auth import AuthService, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["группа авторизации"]
)


@router.post("/sign-up", response_model=TokenModel)
def sing_up(
        user_data: UserCreateModel,
        service: AuthService = Depends()
):
    """
    ## Описание ендпоинта Регистрация поддерживает формат markdown
    \f
    """
    return service.register_new_user(user_data)


@router.post("/sign-in", response_model=TokenModel)
def sing_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends(),
):
    """
    ## Описание ендпоинта Авторизация поддерживает формат markdown
    \f
    """
    return service.authenticate_user(
        username=form_data.username,
        password=form_data.password
    )


@router.get("/user", response_model=UserModel)
def get_user(user: UserModel = Depends(get_current_user)):
    """
    ## Описание ендпоинта Данные пользователя поддерживает формат markdown
    \f
    """
    return user
