# Информация для создания товара
import json
from typing import Optional, Annotated
from pydantic import BaseModel, Field


# Модель для создания товара
class GoodsInit(BaseModel):
    goods_name: Annotated[str, Field(description="Название товара", examples=["Фотоаппарат Sony"],
                                     max_length=100)]
    goods_price: Annotated[str, Field(description="Цена товара", examples=["40,000 рублей"],
                                      max_length=30)]

    goods_small_info: Optional[Annotated[str, Field(description="Краткое описание товара",
                                                    examples=["Очень хороший продукт"])]] = None

    goods_description: Optional[Annotated[dict, Field(description="Полная информация о товаре",
                                                      examples=[{"Цвет": "Синий"}])]] = None

    goods_tag: Optional[Annotated[str, Field(description="Подкатегория товара",
                                             examples=["Фотоаппараты"], max_length=40)]] = None

    goods_img: Annotated[str, Field(description="Адрес до изображения",
                                    examples=["/img.png"], max_length=30)]

    is_visible: Optional[Annotated[bool, Field(description="Видимость товара",
                                               examples=[True])]] = True

    def to_db(self):
        goods = self.model_dump()
        goods_description = goods.get("goods_description", None)

        if goods_description is not None:
            goods["goods_description"] = json.dumps(goods_description)

        return goods

