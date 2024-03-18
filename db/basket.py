from sqlalchemy import text, select

from db.db_init import Session
from db_models.model import Goods
from pydantic_models.customer_model import ResponseBasket


async def basket_customer(user_id: int):
    # выводим корзину пользователя
    async with Session() as session:

        update_query = text(f"SELECT basket FROM customers WHERE customer_id = {user_id}; ")
        res = await session.execute(update_query)

        res = res.fetchone()[0]

        if res == dict():
            res = {"status": "success", "message": "Корзина пуста", "data": {}}

        else:
            res = ResponseBasket(status="success", data=res)
    return res


async def patch_basket(goods_id: int, user_id: int, decrease: bool):
    # изменяем количество товара в корзине +-1
    async with Session() as session:
        res = await session.execute(select(Goods).where(goods_id == Goods.goods_id))
        # товара нет
        if res.fetchone() is None:
            res = {"status": "warning", "message": "Товара не существует"}
            return res

        # получаем старую информацию о корзине
        update_query = text(f"SELECT basket ->> '{goods_id}' FROM customers WHERE customer_id = {user_id}; ")
        res = await session.execute(update_query)

        goods_id = "{" + str(goods_id) + "}"
        res = res.fetchone()[0]
        if res is None:
            res = {"status": "warning", "message": "Товара не было в корзине"}
            return res

        if decrease:
            res = int(res) - 1
            if res == 0:
                update_query = text(
                    "UPDATE customers "
                    f"SET basket = basket #- '{goods_id}' "
                    f"WHERE customer_id = {user_id};"
                )
                await session.execute(update_query)
                await session.commit()
                res = {"status": "success", "message": "Товар успешно удален из корзины"}
                return res

        else:
            res = int(res) + 1

        # обновляем информацию
        update_query = text(
            "UPDATE customers "
            f"SET basket = jsonb_set(basket, '{goods_id}', '{res}', true) "
            f"WHERE customer_id = {user_id};"
        )
        await session.execute(update_query)
        await session.commit()
        res = {"status": "success", "message": "Количество товара изменено в корзине"}
    return res


async def post_basket(goods_id: int, user_id: int, value: int):
    # изменяем количество товара в корзине числом
    async with Session() as session:
        res = await session.execute(select(Goods).where(goods_id == Goods.goods_id))
        # товара нет
        if res.fetchone() is None:
            res = {"status": "warning", "message": "Товара не существует"}
            return res

        goods_id = "{" + str(goods_id) + "}"
        if value == 0:
            update_query = text(
                "UPDATE customers "
                f"SET basket = basket #- '{goods_id}' "
                f"WHERE customer_id = {user_id};"
            )
            await session.execute(update_query)
            await session.commit()
            res = {"status": "success", "message": "Товар успешно удален из корзины"}
            return res

        # обновляем информацию
        update_query = text(
            "UPDATE customers "
            f"SET basket = jsonb_set(basket, '{goods_id}', '{value}', true) "
            f"WHERE customer_id = {user_id};"
        )
        await session.execute(update_query)
        await session.commit()
        res = {"status": "success", "message": "Количество товара изменено в корзине"}
    return res
