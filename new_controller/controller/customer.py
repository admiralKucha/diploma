import json

from fastapi import APIRouter, Response, Cookie
from models.review import Review
from init import databaseCustomer

from auth import customer_required

from models.customer import CustomerChange

customer = APIRouter(prefix="")


@customer.post("/goods/{goods_id}/review", tags=["Покупатель"], summary="Оставить отзыв о товаре")
@customer_required
async def create_review_goods(review: Review, goods_id: int, session: str = Cookie(default=None, include_in_schema=False)):
    review = review.model_dump()
    res = await databaseCustomer.create_review(review, goods_id, session)
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False),
                    status_code=code, media_type='application/json', headers={"Accept": "application/json"})


@customer.post("/goods/{goods_id}/to_basket", tags=["Покупатель"], summary="Положить товар в корзину")
@customer_required
async def to_basket_goods(goods_id: int, session: str = Cookie(default=None, include_in_schema=False)):
    res = await databaseCustomer.to_basket(goods_id, session)
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False),
                    status_code=code, media_type='application/json', headers={"Accept": "application/json"})


@customer.get("/profile", tags=["Покупатель"], summary="Посмотреть данные профиля")
@customer_required
async def check_profile(session: str = Cookie(default=None, include_in_schema=False)):
    res = await databaseCustomer.show_profile(session)
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False),
                    status_code=code, media_type='application/json', headers={"Accept": "application/json"})


@customer.patch("/profile", tags=["Покупатель"], summary="Изменить данные профиля")
@customer_required
async def change_profile(profile: CustomerChange, session: str = Cookie(default=None, include_in_schema=False)):
    profile = profile.model_dump()
    res = await databaseCustomer.change_profile(profile, session)
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False),
                    status_code=code, media_type='application/json', headers={"Accept": "application/json"})


@customer.get("/basket", tags=["Покупатель"], summary="Получить все товары из корзины")
@customer_required
async def show_basket(session: str = Cookie(default=None, include_in_schema=False)):
    res = await databaseCustomer.show_basket(session)
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False),
                    status_code=code, media_type='application/json', headers={"Accept": "application/json"})


@customer.post("/basket/{goods_id}/buy", tags=["Покупатель"], summary="Купить товар из корзины")
@customer_required
async def buy_goods_basket(goods_id: int, city: str, session: str = Cookie(default=None, include_in_schema=False)):
    res = await databaseCustomer.buy_goods(goods_id, session, city)
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False),
                    status_code=code, media_type='application/json', headers={"Accept": "application/json"})


@customer.post("/basket/{goods_id}", tags=["Покупатель"], summary="Изменить количество товаров в корзине")
@customer_required
async def change_goods_basket(goods_id: int, session: str = Cookie(default=None, include_in_schema=False), number=1):
    res = await databaseCustomer.change_basket(goods_id, session, number)
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False),
                    status_code=code, media_type='application/json', headers={"Accept": "application/json"})


@customer.delete("/basket/{goods_id}", tags=["Покупатель"], summary="Удалить товар из корзины")
@customer_required
async def delete_goods_basket(goods_id: int, session: str = Cookie(default=None, include_in_schema=False)):
    res = await databaseCustomer.delete_basket(goods_id, session)
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False),
                    status_code=code, media_type='application/json', headers={"Accept": "application/json"})