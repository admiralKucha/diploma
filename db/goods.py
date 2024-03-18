from sqlalchemy import update, delete, text, select, CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_init import Session
from db_models.model import Goods
from pydantic_models.goods_model import GoodsSmallInfo, GoodsInfo, GoodsInit, GoodsUpdate
from utils.newORM import obj_fetchone, obj_select, obj_fetchall, obj_insert


async def show_goods(offset: int, limit: int, goods_name: str, seller_id: int):
    # список товаров
    async with Session() as session:
        search = f"%{goods_name}%"
        if seller_id is None:
            result = await session.execute(obj_select(Goods, GoodsSmallInfo).
                                           filter(Goods.goods_name.like(search)).offset(offset).limit(limit))
        else:
            result = await session.execute(obj_select(Goods, GoodsSmallInfo).where(Goods.seller_id == seller_id).
                                           filter(Goods.goods_name.like(search)).offset(offset).limit(limit))

        all_goods = obj_fetchall(result, GoodsSmallInfo)
        res = {"status": "success", "data": all_goods}
    return res


async def info_goods(goods_id: int):
    # полная информация об одном товаре
    async with Session() as session:
        result = await session.execute(obj_select(Goods, GoodsInfo).where(Goods.goods_id == goods_id))
        _goods = obj_fetchone(result, GoodsInfo)
        res = {"status": "success", "data": _goods}
    return res


async def buy_goods(goods_id: int, user_id: int):
    # добавляем товар в корзину
    async with Session() as session:
        session: AsyncSession
        res = await session.execute(select(Goods).where(goods_id == Goods.goods_id))
        # товара нет
        if res.fetchone() is None:
            res = {"status": "warning", "message": "Товара не существует"}
            return res

        # получаем старую информацию о корзине
        update_query = text(f"SELECT basket ->> '{goods_id}' FROM customers WHERE customer_id = {user_id}; ")
        res = await session.execute(update_query)

        res = res.fetchone()[0]
        print(res)
        if res is None:
            res = 0

        # добавляем товар
        res = int(res) + 1
        goods_id = "{" + str(goods_id) + "}"

        # обновляем информацию
        update_query = text(
            "UPDATE customers "
            f"SET basket = jsonb_set(basket, '{goods_id}', '{res}', true) "
            f"WHERE customer_id = {user_id};"
        )
        print(update_query)
        await session.execute(update_query)
        await session.commit()
        res = {"status": "success", "message": "Товар успешно добавлен в корзину"}
    return res
