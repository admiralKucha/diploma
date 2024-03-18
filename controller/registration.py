from typing import Union
from fastapi import APIRouter
from pydantic_models.customer_model import CustomerInitPhone, CustomerInitEmail
import db.customers as DBcustomer

registration = APIRouter(prefix="")


@registration.post("/customer", tags=["Регистрация покупателя"])
async def create_customer(customer: Union[CustomerInitPhone, CustomerInitEmail]):
    res = await DBcustomer.create_customer(customer)
    return res
