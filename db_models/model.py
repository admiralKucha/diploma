from enum import Enum

from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Goods(Base):
    __tablename__ = 'goods'

    goods_id = Column(Integer, primary_key=True, autoincrement=True)
    goods_name = Column(String(40), nullable=False)
    goods_description = Column(String)
    goods_price = Column(Integer)
    seller_id = Column(Integer)


# Информация для предпросмотра товаров
class GoodsSmallInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    goods_id: int = Field(description="id Товара", default=12)
    goods_name: str = Field(description="Название товара", default="Товар")
    goods_price: int = Field(description="Цена товара", default=1200)


# Каким может быть статус
class StatusEnum(str, Enum):
    success = "success"
    error = "error"


# Вывод всех товаров
class ResponseGoods(BaseModel):
    status: StatusEnum
    data: list[GoodsSmallInfo]
