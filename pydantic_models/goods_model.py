from enum import Enum
from pydantic import BaseModel, Field


# Информация для предпросмотра товаров
class GoodsSmallInfo(BaseModel):
    goods_id: int = Field(description="id Товара", examples=[12])
    goods_name: str = Field(description="Название товара", examples=["Товар"])
    goods_price: int | None = Field(description="Цена товара", examples=[1200])


# Информация об одном товаре
class GoodsInfo(BaseModel):
    goods_name: str = Field(description="Название товара", default="Товар")
    goods_description: str | None = Field(description="Описание товара", examples=["Описание товара"])
    goods_price: int | None = Field(description="Цена товара", examples=[1200])
    seller_id: int | None = Field(description="id продавца", examples=[12])


# Информация для создания товара
class GoodsInit(BaseModel):
    goods_name: str = Field(description="Название товара", default="Товар")
    goods_description: str | None = Field(description="Описание товара", examples=["Описание товара"])
    goods_price: int | None = Field(description="Цена товара", examples=[1200])
    seller_id: int | None = Field(description="id продавца", examples=[12])


# Каким может быть статус
class StatusEnum(str, Enum):
    success = "success"
    error = "error"


# Вывод всех товаров
class ResponseGoods(BaseModel):
    status: StatusEnum
    data: list[GoodsSmallInfo]


# Вывод полной информации об одном товаре
class ResponseInfoGoods(BaseModel):
    status: StatusEnum
    data: GoodsInfo


# Вывод информации после создания товара
class ResponseCreateGoods(BaseModel):
    status: StatusEnum
    message: str = Field(description="Пояснение к результату выполнения", examples=["Товар успешно создан"])
