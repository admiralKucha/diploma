from datetime import datetime, date
from enum import Enum
from typing import Annotated, Optional
from pydantic import BaseModel, Field


# Информация для регистрации пользователя (телефон)
class CustomerInitPhone(BaseModel):
    phone_number: Annotated[str, Field(description="Номер телефона", examples=["89032001345"],
                                       min_length=11, max_length=11)]


# Информация для регистрации пользователя (email)
class CustomerInitEmail(BaseModel):
    email: Annotated[str, Field(description="Email пользователь", examples=["diploma@mail.ru"],
                                min_length=4, max_length=40)]


# Информация для показа информации пользователю о его профиле
class CustomerInfo(BaseModel):
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


# Информация для обновления информации пользователя
class CustomerUpdate(BaseModel):
    customer_name: Annotated[str, Field(description="Никнейм пользователя", examples=["user-13125345"],
                                        max_length=40)] = None
    birthday: Annotated[date, Field(description="День рождения пользователя",
                                             examples=[datetime.today().date()])] = None
    city: Annotated[str, Field(description="Город пользователя", examples=["Тверь"],
                               max_length=40)] = None


# Каким может быть статус
class StatusEnum(str, Enum):
    success = "success"
    error = "error"
    warning = "warning"


# Вывод информации после регистрации
class ResponseCreateCustomer(BaseModel):
    status: StatusEnum
    message: str = Field(description="Пояснение к результату выполнения", examples=["Пользователь зарегистрирован"])


# Вывод полной информации об пользователе (покупателе)
class ResponseInfoCustomer(BaseModel):
    status: StatusEnum
    data: CustomerInfo


# Вывод информации после обновления информации о пользователе (покупателе)
class ResponseUpdateCustomer(BaseModel):
    status: StatusEnum
    message: str = Field(description="Пояснение к результату выполнения",
                         examples=["Информация о пользователе успешно обновлена"])
