import time

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from db.db_init import Session
from db_models.model import Goods


async def show_goods(offset: int, limit: int):
    start = time.time()
    async with Session() as session:
        session: AsyncSession
        await session.execute(text("SET synchronous_commit TO off;"))
        await session.execute(text("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;"))
        columns = [Goods.goods_id, Goods.goods_name, Goods.goods_price]
        result = await session.execute(select(*columns).offset(offset).limit(limit))
        start = time.time()
        all_goods = result.fetchall()

    return all_goods
