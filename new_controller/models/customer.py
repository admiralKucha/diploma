from datetime import date, datetime
from typing import Optional, Annotated

from pydantic import BaseModel, Field


# Информация для создания аккаунта покупателя

class CustomerInit(BaseModel):
    phone_number: Optional[Annotated[str, Field(description="Номер телефона", examples=["89032001345"],
                                                min_length=11, max_length=11)]]
    email: Optional[Annotated[str, Field(description="Email пользователь", examples=["diploma@mail.ru"],
                                         min_length=4, max_length=40)]]
    customer_name: Annotated[str, Field(description="Никнейм пользователя", examples=["user-13125345"],
                                        max_length=40)]
    birthday: Optional[Annotated[date, Field(description="День рождения пользователя",
                                             examples=[datetime.today().date()])]]
    city: Optional[Annotated[str, Field(description="Город пользователя", examples=["Тверь"],
                                        max_length=40)]]
    password: Annotated[str, Field(description="Пароль пользователя", examples=["1111"])]