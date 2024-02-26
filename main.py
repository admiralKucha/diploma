import asyncio
import time
from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import uvicorn
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi import Request, Form

# то, в чем я правда уверен
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import create_async_engine
from db_models.model import ResponseGoods, GoodsSmallInfo
import db.goods as DBgoods
"""
async def main():
    engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost/diploma", echo=True)
    async with engine.connect() as connection:
        await connection.run_sync(metadata.create_all)

        ins = insert(goods)
        for el in range(0, 100):
            r = await connection.execute(ins, [{"goods_name": "name1"},
                                               {"goods_name": "name2"},
                                               {"goods_name": "name3"},
                                               {"goods_name": "name4"},
                                               {"goods_name": "name5"},
                                               {"goods_name": "name6"},
                                               {"goods_name": "name7"},
                                               {"goods_name": "name8"},
                                               ])

        await connection.commit()
        s = select(goods.c.goods_id)
        r = await connection.execute(s)
        print(len(r.fetchall()))
        engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost/diploma", echo=True)
"""

app = FastAPI()
flag = True

@app.get("/goods/")
async def show_goods(offset: int = 0, limit: int = 10) -> int:
    data = await DBgoods.show_goods(offset, limit)
    data = [GoodsSmallInfo(data=goods) for goods in data]
    res = ResponseGoods(status="success", data=data)
    #await asyncio.sleep(120)
    return 12


# пока мне не нужно
"""
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/auth", response_class=HTMLResponse)
async def auth_form(request: Request):
    return templates.TemplateResponse("auth.html",  {"request": request})


@app.post("/auth", response_class=HTMLResponse)
async def auth_user(request: Request, email: str = Form(...), password: str = Form(...)):
    return templates.TemplateResponse("registration.html", {"request": request, "email": email})


@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("registration.html",  {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
"""
