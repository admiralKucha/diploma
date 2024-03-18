from fastapi import APIRouter
import db.basket as DBbasket


basket = APIRouter(prefix="/{customer_id}/basket")


@basket.get("", tags=["Покупатель-Корзина"])
async def basket_customer(customer_id: int):
    res = await DBbasket.basket_customer(customer_id)
    return res


@basket.patch("/{goods_id}", tags=["Покупатель-Корзина"])
async def patch_basket(customer_id: int, goods_id: int, decrease: bool = False):
    res = await DBbasket.patch_basket(goods_id, customer_id, decrease)

    return res


@basket.post("/{goods_id}", tags=["Покупатель-Корзина"])
async def post_basket(customer_id: int, goods_id: int, value: int):
    if value < 0:
        value = 0
    res = await DBbasket.post_basket(goods_id, customer_id, value)
    return res
