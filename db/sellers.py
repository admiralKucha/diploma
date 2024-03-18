from sqlalchemy import insert, update, delete, and_
from db.db_init import Session
from db_models.model import Sellers, Goods
from pydantic_models.goods_model import GoodsSmallInfo, GoodsInit, GoodsUpdate, GoodsInfo, GoodsSmallInfoSeller, \
    GoodsInfoSeller, ResponseGoodsSeller, ResponseInfoGoodsSeller
from pydantic_models.seller_model import SellerInit, SellerInfo, SellerShow, ResponseInfoSeller
from utils.newORM import obj_select, obj_fetchone, obj_fetchall, obj_insert


async def info_seller(seller_id: int):
    # полная информация о пользователе
    async with Session() as session:
        result = await session.execute(obj_select(Sellers, SellerInfo).where(Sellers.seller_id == seller_id))
        _seller = obj_fetchone(result, SellerInfo)
        res = ResponseInfoSeller(status="success", data=_seller)
    return res


async def show_goods(offset: int, limit: int, goods_name: str, seller_id: int):
    # список товаров
    async with Session() as session:
        search = f"%{goods_name}%"
        result = await session.execute(obj_select(Goods, GoodsSmallInfoSeller).where(Goods.seller_id == seller_id).
                                       filter(Goods.goods_name.like(search)).offset(offset).limit(limit))

        all_goods = obj_fetchall(result, GoodsSmallInfoSeller)
        res = ResponseGoodsSeller(status="success", data=all_goods)
    return res


async def create_goods(goods: GoodsInit):
    async with Session() as session:
        await session.execute(*obj_insert(Goods, [goods]))
        await session.commit()
        res = {"status": "success", "message": "Товар успешно создан"}

    return res


async def update_goods(goods_id: int, seller_id: int,  goods: GoodsUpdate):
    # обновляем товар
    async with Session() as session:
        values = goods.model_dump(exclude_unset=True)
        if len(values) == 0:
            res = {"status": "warning", "message": "Не поступило изменений"}
            return res

        res = await session.execute(update(Goods).
                                    where(and_(goods_id == Goods.goods_id, seller_id == Goods.seller_id)).
                                    values(values).
                                    returning(Goods.goods_id))

        # товара нет
        if res.fetchone() is None:
            res = {"status": "warning", "message": "Товара не существует"}
            return res

        await session.commit()
        res = {"status": "success", "message": "Товар успешно обновлен"}
    return res


async def delete_goods(goods_id: int, seller_id: int):
    # удаляем товар
    async with Session() as session:
        res = await session.execute(delete(Goods).
                                    where(and_(goods_id == Goods.goods_id, seller_id == Goods.seller_id)).
                                    returning(Goods.goods_id))

        # товара нет
        if res.fetchone() is None:
            res = {"status": "warning", "message": "Товара не существовало"}
            return res

        await session.commit()
        res = {"status": "success", "message": "Товар успешно удален"}
    return res


async def info_goods(goods_id: int, seller_id: int):
    # полная информация об одном товаре
    async with Session() as session:
        result = await session.execute(obj_select(Goods, GoodsInfoSeller).
                                       where(and_(Goods.goods_id == goods_id, Goods.seller_id == seller_id)))
        _goods = obj_fetchone(result, GoodsInfoSeller)
        if _goods is None:
            res = {"status": "warning", "message": "Такого товара нет"}
        else:
            res = ResponseInfoGoodsSeller(status="success", data=_goods)
    return res

