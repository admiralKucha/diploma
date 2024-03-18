from sqlalchemy import insert
from db.db_init import Session
from db_models.model import Sellers
from pydantic_models.seller_model import SellerInit


async def create_seller(seller: SellerInit):
    # администратор регистрирует пользователя
    async with Session() as session:
        await session.execute(insert(Sellers).values(**seller.model_dump()))
        await session.commit()
        res = {"status": "success", "message": "Продавец зарегистрирован"}

    return res