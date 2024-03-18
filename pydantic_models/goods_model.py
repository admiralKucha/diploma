from enum import Enum
from typing import Annotated, Union, Optional

from pydantic import BaseModel, Field


# Информация для предпросмотра товаров
class GoodsSmallInfo(BaseModel):
    goods_id: int = Field(description="id Товара", examples=[12])
    goods_name: str = Field(description="Название товара", examples=["Товар"])
    goods_price: int | None = Field(description="Цена товара", examples=[1200])
    seller_id: int | None = Field(description="id продавца", examples=[12])


# Информация об одном товаре
class GoodsInfo(BaseModel):
    goods_name: str = Field(description="Название товара", default="Товар")
    goods_description: str | None = Field(description="Описание товара", examples=["Описание товара"])
    goods_price: int | None = Field(description="Цена товара", examples=[1200])
    seller_id: int | None = Field(description="id продавца", examples=[12])


# Информация краткая информация о товаре для продавца
class GoodsSmallInfoSeller(BaseModel):
    goods_id: int = Field(description="id Товара", examples=[12])
    goods_name: str = Field(description="Название товара", default="Товар")
    goods_price: int | None = Field(description="Цена товара", examples=[1200])
    is_visible: Optional[Annotated[bool, Field(description="Опубликован ли товар", examples=[True])]] = None


# Информация об одном товаре для продавца
class GoodsInfoSeller(BaseModel):
    goods_name: str = Field(description="Название товара", default="Товар")
    goods_description: str | None = Field(description="Описание товара", examples=["Описание товара"])
    goods_price: int | None = Field(description="Цена товара", examples=[1200])
    is_visible: Optional[Annotated[bool, Field(description="Опубликован ли товар", examples=[True])]] = None


# Информация для создания товара
class GoodsInit(BaseModel):
    goods_name: str = Field(description="Название товара", default="Товар")
    goods_description: str | None = Field(description="Описание товара", examples=["Описание товара"])
    goods_price: int | None = Field(description="Цена товара", examples=[1200])
    seller_id: int | None = Field(description="id продавца", examples=[12])
    is_visible: Optional[Annotated[bool, Field(description="Опубликован ли товар", examples=[True])]] = None


# Информация для обновления одного товара
class GoodsUpdate(BaseModel):
    goods_name: Annotated[str, Field(description="Название товара", default="Товар")] = None
    goods_description: Optional[Annotated[str, Field(description="Описание товара", examples=["Описание товара"])]] = None
    goods_price: Optional[Annotated[int, Field(description="Цена товара", examples=[1200])]] = None
    is_visible: Optional[Annotated[bool, Field(description="Опубликован ли товар", examples=[True])]] = None


# Каким может быть статус
class StatusEnum(str, Enum):
    success = "success"
    error = "error"
    warning = "warning"


# Вывод всех товаров
class ResponseGoods(BaseModel):
    status: StatusEnum
    data: list[GoodsSmallInfo]


# Вывод всех товаров
class ResponseGoodsSeller(BaseModel):
    status: StatusEnum
    data: list[GoodsSmallInfoSeller]


# Вывод полной информации об одном товаре
class ResponseInfoGoods(BaseModel):
    status: StatusEnum
    data: GoodsInfo


# Вывод полной информации об одном товаре для продавца
class ResponseInfoGoodsSeller(BaseModel):
    status: StatusEnum
    data: GoodsInfoSeller


# Вывод информации после создания товара
class ResponseCreateGoods(BaseModel):
    status: StatusEnum
    message: str = Field(description="Пояснение к результату выполнения", examples=["Товар успешно создан"])


# Вывод информации после обновления товара
class ResponseUpdateGoods(BaseModel):
    status: StatusEnum
    message: str = Field(description="Пояснение к результату выполнения", examples=["Товар успешно обновлен"])


# Вывод информации после удаления отзыва
class ResponseDeleteGoods(BaseModel):
    status: StatusEnum
    message: str = Field(description="Пояснение к результату выполнения", examples=["Товар успешно удален"])


# Вывод информации после добавления в корзину
class ResponseBuyGoods(BaseModel):
    status: StatusEnum
    message: str = Field(description="Пояснение к результату выполнения", examples=["Товар успешно добавлен в корзину"])
