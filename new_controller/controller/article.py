from fastapi import APIRouter, Response, Cookie


article = APIRouter(prefix="")


@article.get("/articles", tags=["Статьи"], summary="Посмотреть список статей")
async def show_articles():
    pass
    return 212


@article.get("/articles/{article_id}", tags=["Статьи"], summary="Получить информацию об определенной статье")
async def show_id_article(article_id_: int):
    pass
    return 212
