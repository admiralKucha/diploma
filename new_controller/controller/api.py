from fastapi import APIRouter

from . import admin, article, customer, goods, user

api = APIRouter(prefix="/api")

api.include_router(admin.admin)
api.include_router(article.article)
api.include_router(customer.customer)
api.include_router(goods.goods)
api.include_router(user._user)

