from fastapi import APIRouter, Response, Cookie


goods = APIRouter(prefix="")


@goods.get("/goods", tags=["Товары"], summary="Посмотреть все товары")
async def show_goods():
    pass
    return 212


@goods.get("/goods/{goods_id}", tags=["Товары"], summary="Посмотреть определенный товар")
async def show_id_goods(goods_id: int):
    pass
    return 212


@goods.get("/goods/tags", tags=["Товары"], summary="Посмотреть подкатегории товаров")
async def show_tags_goods(goods_id: int):
    pass
    return 212