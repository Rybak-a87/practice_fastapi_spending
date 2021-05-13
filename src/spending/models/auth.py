from pydantic import BaseModel


class BaseUserModel(BaseModel):
    email: str
    username: str


class UserCreateModel(BaseUserModel):
    password: str


class UserModel(BaseUserModel):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    """
    модель с токеном
    """
    access_token: str    # в нем будет лежать jwt
    token_type: str = "bearer"