import json

from fastapi import APIRouter, Response, Cookie

from models.goods import GoodsInit
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
async def change_goods(goods_id: int, session: str = Cookie(default=None, include_in_schema=False)):
    pass
    return 212


@admin.delete("/goods/{goods_id}", tags=["Админ"], summary="Удалить товар")
async def delete_goods(goods_id: int, session: str = Cookie(default=None, include_in_schema=False)):
    pass
    return 212


@admin.post("/articles", tags=["Админ"], summary="Создать статьи")
async def create_article(session: str = Cookie(default=None, include_in_schema=False)):
    pass
    return 212


@admin.patch("/articles/{article_id}", tags=["Админ"], summary="Изменить статью")
async def patch_article(article_id: int, session: str = Cookie(default=None, include_in_schema=False)):
    pass
    return 212


@admin.delete("/articles/{article_id}", tags=["Админ"], summary="Удалить статью")
async def delete_article(article_id: int, session: str = Cookie(default=None, include_in_schema=False)):
    pass
    return 212


@admin.get("/stats", tags=["Админ"], summary="Посмотреть статистику сайта")
async def show_stats(session: str = Cookie(default=None, include_in_schema=False)):
    pass
    return 212