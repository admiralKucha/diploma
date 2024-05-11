# -*- coding: utf-8 -*-
from fastapi import FastAPI
from controller.api import api
from init import router

app = FastAPI()

app.include_router(api)
app.include_router(router)

