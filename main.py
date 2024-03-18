from typing import Union

from fastapi import FastAPI, Query

from controller import admin, seller, registration, customer, goods

from db.db_init import sync_engine
from db_models.model import Base


app = FastAPI()
app.include_router(admin.admin)
app.include_router(seller.seller)
app.include_router(registration.registration)
app.include_router(customer._customer)
app.include_router(goods._goods)

Base.metadata.create_all(sync_engine, checkfirst=True)

