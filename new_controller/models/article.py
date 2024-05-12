from typing import Annotated

from pydantic import BaseModel, Field


# Модель для создания статьи
class ArticleInit(BaseModel):
    article_title: Annotated[str, Field(description="Название статьи", examples=["Название статьи"],
                                        max_length=100)]

    article_small_info: Annotated[str, Field(description="Краткое описание статьи",
                                             examples=["Краткое описание статьи"])]

    article_text: Annotated[str, Field(description="Полная текст статьи", examples=["Полная текст статьи"])]

    is_visible: Annotated[bool, Field(description="Видимость товара", examples=[True])] = True


# Модель для изменения статьи
class ArticleChange(BaseModel):

    article_small_info: Annotated[str, Field(description="Краткое описание статьи",
                                             examples=["Краткое описание статьи"])]

    article_text: Annotated[str, Field(description="Полная текст статьи", examples=["Полная текст статьи"])]

    is_visible: Annotated[bool, Field(description="Видимость товара", examples=[True])] = True
