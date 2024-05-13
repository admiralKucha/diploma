import json

from fastapi import APIRouter, Response, Cookie

from init import databaseGuest

goods = APIRouter(prefix="")


@goods.get("/goods", tags=["Товары"], summary="Посмотреть все товары")
async def show_goods(session: str = Cookie(default=None, include_in_schema=False)):
    res = await databaseGuest.show_all_goods()
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False),
                    status_code=code, media_type='application/json', headers={"Accept": "application/json"})


@goods.get("/goods/tags", tags=["Товары"], summary="Посмотреть подкатегории товаров")
async def show_tags_goods(session: str = Cookie(default=None, include_in_schema=False)):
    res = await databaseGuest.show_all_tags()
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False),
                    status_code=code, media_type='application/json', headers={"Accept": "application/json"})


@goods.get("/goods/{goods_id}", tags=["Товары"], summary="Посмотреть определенный товар")
async def show_id_goods(goods_id: int, session: str = Cookie(default=None, include_in_schema=False)):
    res = await databaseGuest.show_id_goods(goods_id)
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False),
                    status_code=code, media_type='application/json', headers={"Accept": "application/json"})
