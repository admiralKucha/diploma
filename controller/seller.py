from fastapi import APIRouter

from pydantic_models.goods_model import ResponseGoods, GoodsInit, ResponseCreateGoods, GoodsUpdate, ResponseUpdateGoods, \
    ResponseDeleteGoods, ResponseInfoGoods, ResponseGoodsSeller, ResponseInfoGoodsSeller
from pydantic_models.seller_model import ResponseInfoSeller
import db.sellers as DBseller

seller = APIRouter(prefix="/seller")


@seller.get("", tags=["Продавец"])
async def seller_info_seller(seller_id: int) -> ResponseInfoSeller:
    res = await DBseller.info_seller(seller_id)
    return res


@seller.get("/goods", tags=["Продавец"])
async def seller_show_goods(seller_id: int,
                            offset: int = 0, limit: int = 10,
                            goods_name: str = ""):

    res = await DBseller.show_goods(offset, limit, goods_name, seller_id)
    return res


@seller.post("/goods",  tags=["Продавец"])
async def seller_create_goods(goods: GoodsInit):
    res = await DBseller.create_goods(goods)
    return res


@seller.get("/goods/{goods_id}",  tags=["Продавец"])
async def seller_info_goods(goods_id: int, seller_id: int):
    res = await DBseller.info_goods(goods_id, seller_id)
    return res


@seller.patch("/goods/{goods_id}",  tags=["Продавец"])
async def seller_update_goods(goods_id: int, seller_id: int, goods: GoodsUpdate):
    res = await DBseller.update_goods(goods_id, seller_id, goods)
    return res


@seller.delete("/goods/{goods_id}",  tags=["Продавец"])
async def seller_delete_goods(goods_id: int, seller_id: int):
    res = await DBseller.delete_goods(goods_id, seller_id)
    return res
