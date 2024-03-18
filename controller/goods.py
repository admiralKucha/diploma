from fastapi import APIRouter
import db.goods as DBgoods
import db.reviews as DBreviews
from pydantic_models.reviews_model import ReviewUpdate, ReviewInfo

_goods = APIRouter(prefix="/goods")


@_goods.get("/goods", tags=["Товары"])
async def show_goods(offset: int = 0, limit: int = 10, goods_name: str = "", seller_id: int = None):
    res = await DBgoods.show_goods(offset, limit, goods_name, seller_id)
    return res


@_goods.get("/goods/{goods_id}", tags=["Товары"])
async def info_goods(goods_id: int):
    res = await DBgoods.info_goods(goods_id)
    return res


@_goods.get("/goods/{goods_id}/buy", tags=["Товары"])
async def buy_goods(goods_id: int, user_id: int):
    res = await DBgoods.buy_goods(goods_id, user_id)
    return res


@_goods.get("/goods/{goods_id}/reviews", tags=["Товары"])
async def show_reviews(goods_id: int, offset: int = 0, limit: int = 10):
    res = await DBreviews.show_reviews(goods_id, offset, limit)
    return res


@_goods.post("/goods/{goods_id}/reviews", tags=["Товары"])
async def create_review(reviews: ReviewInfo, goods_id: int):
    res = await DBreviews.create_review(reviews, goods_id)
    return res


@_goods.delete("/goods/{goods_id}/reviews", tags=["Товары"])
async def delete_review(goods_id: int, user_id: int):
    res = await DBreviews.delete_review(goods_id, user_id)
    return res


@_goods.patch("/goods/{goods_id}/reviews", tags=["Товары"])
async def update_review(goods_id: int, user_id: int, review: ReviewUpdate):
    res = await DBreviews.update_review(goods_id, user_id, review)
    return res
