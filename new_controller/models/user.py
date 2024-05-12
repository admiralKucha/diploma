from typing import Annotated
from pydantic import BaseModel, Field, EmailStr


# Информация, необходимая для авторизации
class UserAuth(BaseModel):
    username: Annotated[str,  Field(min_length=4, max_length=40, examples=["test@test.ru"])]
    password: str


# Информация о юзере
class UserLoaded(BaseModel):
    global_id: int
    username: str
    user_group: int


