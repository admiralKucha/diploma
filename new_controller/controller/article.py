import json

from fastapi import APIRouter, Response, Cookie

from init import databaseGuest

article = APIRouter(prefix="")


@article.get("/articles", tags=["Статьи"], summary="Посмотреть список статей")
async def show_articles(session: str = Cookie(default=None, include_in_schema=False)):
    res = await databaseGuest.show_all_article()
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False),
                    status_code=code, media_type='application/json', headers={"Accept": "application/json"})


@article.get("/articles/{article_id}", tags=["Статьи"], summary="Получить информацию об определенной статье")
async def show_id_article(article_id: int, session: str = Cookie(default=None, include_in_schema=False)):
    res = await databaseGuest.show_id_article(article_id)
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False),
                    status_code=code, media_type='application/json', headers={"Accept": "application/json"})
