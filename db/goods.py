from db.db_init import Session
from db_models.model import Goods
from pydantic_models.goods_model import GoodsSmallInfo, GoodsInfo, GoodsInit
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
