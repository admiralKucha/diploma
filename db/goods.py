from sqlalchemy import update, delete

from db.db_init import Session
from db_models.model import Goods
from pydantic_models.goods_model import GoodsSmallInfo, GoodsInfo, GoodsInit, GoodsUpdate
from utils.newORM import obj_fetchone, obj_select, obj_fetchall, obj_insert


async def show_goods(offset: int, limit: int):
    # список товаров
    async with Session() as session:
        result = await session.execute(obj_select(Goods, GoodsSmallInfo).offset(offset).limit(limit))
        all_goods = obj_fetchall(result, GoodsSmallInfo)
    return all_goods


async def info_goods(goods_id: int):
    # полная информация об одном товаре
    async with Session() as session:
        result = await session.execute(obj_select(Goods, GoodsInfo).where(Goods.goods_id == goods_id))
        _goods = obj_fetchone(result, GoodsInfo)
    return _goods


async def create_goods(goods: GoodsInit):
    async with Session() as session:
        await session.execute(*obj_insert(Goods, [goods]))
        await session.commit()
        res = {"status": "success", "message": "Товар успешно создан"}

    return res


async def update_goods(goods_id: int, goods: GoodsUpdate):
    # обновляем товар
    async with Session() as session:
        values = goods.model_dump(exclude_unset=True)
        if len(values) == 0:
            res = {"status": "warning", "message": "Не поступило изменений"}
            return res

        res = await session.execute(update(Goods).
                                    where(goods_id == Goods.goods_id).
                                    values(values).
                                    returning(Goods.goods_id))

        # товара нет
        if res.fetchone() is None:
            res = {"status": "warning", "message": "Товара не существует"}
            return res

        await session.commit()
        res = {"status": "success", "message": "Товар успешно обновлен"}
    return res


async def delete_goods(goods_id: int):
    # удаляем товар
    async with Session() as session:
        res = await session.execute(delete(Goods).
                                    where(goods_id == Goods.goods_id).
                                    returning(Goods.goods_id))

        # товара нет
        if res.fetchone() is None:
            res = {"status": "warning", "message": "Товара не существовало"}
            return res

        await session.commit()
        res = {"status": "success", "message": "Товар успешно удален"}
    return res
