from enum import Enum
from typing import Annotated, List
from pydantic import BaseModel, Field


class SellerInit(BaseModel):
    seller_name: Annotated[str, Field(description="Название компании", examples=["Yellow store"],
                                      min_length=1, max_length=40)]


class SellerInfo(BaseModel):
    seller_name: Annotated[str, Field(description="Название компании", examples=["Yellow store"],
                                      min_length=1, max_length=40)]


class SellerShow(BaseModel):
    seller_id: int
    seller_name: Annotated[str, Field(description="Название компании", examples=["Yellow store"],
                                      min_length=1, max_length=40)]


# Каким может быть статус
class StatusEnum(str, Enum):
    success = "success"
    error = "error"
    warning = "warning"


# Вывод информации после регистрации
class ResponseCreateSeller(BaseModel):
    status: StatusEnum
    message: str = Field(description="Пояснение к результату выполнения", examples=["Продавец зарегистрирован"])


# Вывод полной информации об пользователе (продавцец)
class ResponseInfoSeller(BaseModel):
    status: StatusEnum
    data: SellerInfo


# Вывод информацию о продавцах
class ResponseSellers(BaseModel):
    status: StatusEnum
    data: List[SellerShow]


