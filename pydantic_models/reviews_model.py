from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, Field


# Информация для создания отклика
class ReviewInit(BaseModel):
    goods_id: Annotated[int, Field(description="id Товара", examples=[12])]
    user_id: Annotated[int, Field(description="id Пользователя, который пишет обзор", examples=[12])]
    review: Annotated[str, Field(description="Текст обзора", examples=["Текст обзора"])]
    stars: Annotated[int, Field(description="Количество звезд", examples=[3], ge=1, le=5)]


# Информация для просмотра обзоров на товар
class ReviewInfo(BaseModel):
    user_id: Annotated[int, Field(description="id Пользователя, который пишет обзор", examples=[12])]
    review: Annotated[str, Field(description="Текст обзора", examples=["Текст обзора"])]
    stars: Annotated[int, Field(description="Количество звезд", examples=[3], ge=1, le=5)]


# Информация для изменения обзора на товар
class ReviewUpdate(BaseModel):
    review: Annotated[str, Field(description="Текст обзора", examples=["Текст обзора"])] = None
    stars: Annotated[int, Field(description="Количество звезд", examples=[3], ge=1, le=5)] = None


# Каким может быть статус
class StatusEnum(str, Enum):
    success = "success"
    error = "error"
    warning = "warning"


# Вывод информации после создания отзыва
class ResponseCreateReview(BaseModel):
    status: StatusEnum
    message: str = Field(description="Пояснение к результату выполнения", examples=["Обзор успешно оставлен"])


# Вывод информации о всех отзывах на товар
class ResponseReviews(BaseModel):
    status: StatusEnum
    data: list[ReviewInfo]


# Вывод информации после удаления отзыва
class ResponseDeleteReview(BaseModel):
    status: StatusEnum
    message: str = Field(description="Пояснение к результату выполнения", examples=["Обзор успешно удален"])


# Вывод информации после обновления отзыва
class ResponseUpdateReview(BaseModel):
    status: StatusEnum
    message: str = Field(description="Пояснение к результату выполнения", examples=["Обзор успешно обновлен"])


