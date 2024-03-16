from sqlalchemy import insert
from db.db_init import Session
from db_models.model import Sellers
from pydantic_models.seller_model import SellerInit, SellerInfo, SellerShow
from utils.newORM import obj_select, obj_fetchone, obj_fetchall


async def create_seller(seller: SellerInit):
    # администратор регистрирует пользователя
    async with Session() as session:
        await session.execute(insert(Sellers).values(**seller.model_dump()))
        await session.commit()
        res = {"status": "success", "message": "Продавец зарегистрирован"}

    return res


async def info_seller(seller_id: int):
    # полная информация о пользователе
    async with Session() as session:
        result = await session.execute(obj_select(Sellers, SellerInfo).where(Sellers.seller_id == seller_id))
        _customer = obj_fetchone(result, SellerInfo)
    return _customer


async def show_sellers(offset: int, limit: int, seller_name: str):
    # список продавцов
    async with Session() as session:
        search = f"%{seller_name}%"
        result = await session.execute(obj_select(Sellers, SellerShow).
                                       filter(Sellers.seller_name.like(search)).offset(offset).limit(limit))

        all_goods = obj_fetchall(result, SellerShow)
    return all_goods
