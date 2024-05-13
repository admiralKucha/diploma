from datetime import date, datetime
from typing import Optional, Annotated

from pydantic import BaseModel, Field


# Информация для создания отзыва о товаре

class Review(BaseModel):
    stars: Annotated[str, Field(description="Рейтинг товара", examples=["5 звезд"], max_length=40)]

    customer_text: Annotated[str, Field(description="Текст отзыва", examples=["Текст отзыва"])]