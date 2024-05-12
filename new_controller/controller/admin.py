import json

from fastapi import APIRouter, Response, Cookie

from models.goods import GoodsInit
from models.article import ArticleInit, ArticleChange
from init import databaseAdmin


admin = APIRouter(prefix="")


@admin.post("/goods", tags=["Админ"], summary="Создать товар")
async def create_goods(goods: GoodsInit, session: str = Cookie(default=None, include_in_schema=False)):
    goods = goods.to_db()
    res = await databaseAdmin.create_new_goods(goods)
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False),
                    status_code=code, media_type='application/json', headers={"Accept": "application/json"})


@admin.patch("/goods/{goods_id}", tags=["Админ"], summary="Изменить определенный товар")
async def change_goods(goods: GoodsInit, goods_id: int, session: str = Cookie(default=None, include_in_schema=False)):
    goods = goods.to_db()
    res = await databaseAdmin.change_goods(goods, goods_id)
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False),
                    status_code=code, media_type='application/json', headers={"Accept": "application/json"})


@admin.delete("/goods/{goods_id}", tags=["Админ"], summary="Удалить товар")
async def delete_goods(goods_id: int, session: str = Cookie(default=None, include_in_schema=False)):
    res = await databaseAdmin.delete_goods(goods_id)
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False),
                    status_code=code, media_type='application/json', headers={"Accept": "application/json"})


@admin.post("/articles", tags=["Админ"], summary="Создать статьи")
async def create_article(article: ArticleInit, session: str = Cookie(default=None, include_in_schema=False)):
    article = article.model_dump()
    res = await databaseAdmin.create_new_article(article)
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False),
                    status_code=code, media_type='application/json', headers={"Accept": "application/json"})


@admin.patch("/articles/{article_id}", tags=["Админ"], summary="Изменить статью")
async def patch_article(article: ArticleChange, article_id: int, session: str = Cookie(default=None, include_in_schema=False)):
    article = article.model_dump()
    res = await databaseAdmin.change_article(article, article_id)
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False),
                    status_code=code, media_type='application/json', headers={"Accept": "application/json"})


@admin.delete("/articles/{article_id}", tags=["Админ"], summary="Удалить статью")
async def delete_article(article_id: int, session: str = Cookie(default=None, include_in_schema=False)):
    res = await databaseAdmin.delete_article(article_id)
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False),
                    status_code=code, media_type='application/json', headers={"Accept": "application/json"})


@admin.get("/stats", tags=["Админ"], summary="Посмотреть статистику сайта")
async def show_stats(session: str = Cookie(default=None, include_in_schema=False)):
    pass
    return 212