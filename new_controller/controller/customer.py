from fastapi import APIRouter, Response, Cookie


customer = APIRouter(prefix="")


@customer.post("/goods/{goods_id}/review", tags=["Покупатель"], summary="Оставить отзыв о товаре")
async def create_review_goods(goods_id: int):
    pass
    return 212


@customer.post("/goods/{goods_id}/to_basket", tags=["Покупатель"], summary="Положить товар в корзину")
async def to_basket_goods(goods_id: int):
    pass
    return 212


@customer.get("/profile", tags=["Покупатель"], summary="Посмотреть данные профиля")
async def check_profile():
    pass
    return 212


@customer.post("/profile", tags=["Покупатель"], summary="Изменить данные профиля")
async def change_profile():
    pass
    return 212


@customer.get("/basket", tags=["Покупатель"], summary="Получить все товары из корзины")
async def show_basket():
    pass
    return 212


@customer.post("/basket/{goods_id}/buy", tags=["Покупатель"], summary="Купить товар из корзины")
async def buy_goods_basket():
    pass
    return 212


@customer.post("/basket/{goods_id}", tags=["Покупатель"], summary="Изменить количество товаров в корзине")
async def buy_goods_basket():
    pass
    return 212


@customer.delete("/basket/{goods_id}", tags=["Покупатель"], summary="Удалить товар из корзины")
async def delete_goods_basket():
    pass
    return 212