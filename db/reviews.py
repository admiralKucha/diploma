from sqlalchemy import select, and_, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_init import Session
from db_models.model import Reviews, Goods
from pydantic_models.reviews_model import ReviewInit, ReviewInfo, ReviewUpdate
from utils.newORM import obj_insert, obj_select, obj_fetchall


async def create_review(reviews: ReviewInfo, goods_id: int):
    async with Session() as session:
        # проверяем, есть ли товар
        flag = await session.execute(select(*[Goods.goods_id]).where(goods_id == Goods.goods_id))
        if not flag.fetchone():
            res = {"status": "error", "message": "Такого товара нет"}
            return res

        # проверяем, есть ли уже обзор на данный товар от данного пользователя
        flag = await session.execute(select(*[Reviews.goods_id, Reviews.user_id]).where(
            and_(goods_id == Reviews.goods_id, reviews.user_id == Reviews.user_id)))
        if flag.fetchone():
            await session.execute(update(Reviews).
                                  where(and_(goods_id == Reviews.goods_id, reviews.user_id == Reviews.user_id)).
                                  values(reviews.model_dump()))
            await session.commit()
            res = {"status": "success", "message": "Обзор успешно обновлен"}
            return res

        await session.execute(insert(Reviews).values({"goods_id": goods_id, **reviews.model_dump()}))
        await session.commit()
        res = {"status": "success", "message": "Обзор успешно оставлен"}

    return res


async def show_reviews(goods_id: int, offset: int, limit: int):
    # список обзоров
    async with Session() as session:
        result = await session.execute(obj_select(Reviews, ReviewInfo).
                                       where(goods_id == Reviews.goods_id).offset(offset).limit(limit))
        all_reviews = obj_fetchall(result, ReviewInfo)
    return all_reviews


async def delete_review(goods_id: int, user_id: int):
    # удаляем обзор
    async with Session() as session:
        res = await session.execute(delete(Reviews).
                                    where(and_(goods_id == Reviews.goods_id, user_id == Reviews.user_id)).
                                    returning(Reviews.goods_id))

        # обзора нет
        if res.fetchone() is None:
            res = {"status": "warning", "message": "Обзора не существовало"}
            return res

        await session.commit()
        res = {"status": "success", "message": "Обзор успешно удален"}
    return res


async def update_review(goods_id: int, user_id: int, review: ReviewUpdate):
    # обновляем обзор
    async with Session() as session:
        values = {key: value for key, value in review.model_dump().items() if value is not None}
        if len(values) == 0:
            res = {"status": "warning", "message": "Не поступило изменений"}
            return res

        res = await session.execute(update(Reviews).
                                    where(and_(goods_id == Reviews.goods_id, user_id == Reviews.user_id)).
                                    values(values).
                                    returning(Reviews.goods_id))

        # обзора нет
        if res.fetchone() is None:
            res = {"status": "warning", "message": "Обзора не существует"}
            return res

        await session.commit()
        res = {"status": "success", "message": "Обзор успешно обновлен"}
    return res
