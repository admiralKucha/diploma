import random
import string
from typing import Union
from sqlalchemy import insert, select, update, and_, text
from db.db_init import Session
from db_models.model import Customers, Goods
from pydantic_models.customer_model import CustomerInitPhone, CustomerInitEmail, CustomerInfo, CustomerUpdate
from utils.newORM import obj_select, obj_fetchone


async def create_customer(customers: Union[CustomerInitPhone, CustomerInitEmail]):
    async with Session() as session:
        # по номеру телефона?
        if isinstance(customers, CustomerInitPhone):
            flag = await session.execute(select(1).where(
                (Customers.phone_number == customers.phone_number)))
            if flag.fetchone():
                return {"status": "error", "message": "Такой номер телефона уже есть"}

        # по почте?
        else:
            flag = await session.execute(select(1).where(
                (Customers.email == customers.email)))
            if flag.fetchone():
                return {"status": "error", "message": "Такая почта уже есть"}

        # Создаем никнейм
        flag = True
        while flag:
            name = "user-" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            flag = await session.execute(select(1).where(
                (Customers.customer_name == name)))

            flag = flag.fetchone()

        await session.execute(insert(Customers).values({**customers.model_dump(), "customer_name": name}))
        await session.commit()
        res = {"status": "success", "message": "Пользователь зарегистрирован"}

    return res


async def info_customer(customer_id: int):
    # полная информация о пользователе
    async with Session() as session:
        result = await session.execute(obj_select(Customers, CustomerInfo).where(Customers.customer_id == customer_id))
        _customer = obj_fetchone(result, CustomerInfo)
    return _customer


async def update_customer(customer_id: int, customer: CustomerUpdate):
    # обновляем обзор
    async with Session() as session:
        values = customer.model_dump(exclude_unset=True)
        if len(values) == 0:
            res = {"status": "warning", "message": "Не поступило изменений"}
            return res

        res = await session.execute(update(Customers).
                                    where(customer_id == Customers.customer_id).
                                    values(values).
                                    returning(Customers.customer_id))

        # Пользователя нет (вероятно не нужно)
        if res.fetchone() is None:
            res = {"status": "warning", "message": "Пользователя не существует"}
            return res

        await session.commit()
        res = {"status": "success", "message": "Информация о пользователе обновлена"}
    return res


async def basket_customer(user_id: int):
    # выводим корзину пользователя
    async with Session() as session:

        update_query = text(f"SELECT basket FROM customers WHERE customer_id = {user_id}; ")
        res = await session.execute(update_query)

        res = res.fetchone()[0]
        print(res)
        if res is None:
            res = dict()

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



