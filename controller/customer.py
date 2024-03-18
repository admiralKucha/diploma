from fastapi import APIRouter
import db.customers as DBcustomer
from controller import basket
from pydantic_models.customer_model import CustomerUpdate


_customer = APIRouter(prefix="/customer")


@_customer.get("/show_sellers", tags=["Покупатель-Список продавцов"])
async def show_sellers(offset: int = 0, limit: int = 10, seller_name: str = ""):
    res = await DBcustomer.show_sellers(offset, limit, seller_name)
    return res


@_customer.get("/{customer_id}", tags=["Покупатель-Личная Информация"])
async def info_customer(customer_id: int):
    res = await DBcustomer.info_customer(customer_id)
    return res


@_customer.patch("/{customer_id}", tags=["Покупатель-Личная Информация"])
async def update_customer(customer_id: int, customer: CustomerUpdate):
    res = await DBcustomer.update_customer(customer_id, customer)
    return res

_customer.include_router(basket.basket)

