from fastapi import FastAPI, Query

# то, в чем я правда уверен
import db.goods as DBgoods
import db.reviews as DBreviews
from db.db_init import sync_engine
from db_models.model import Base
from pydantic_models.goods_model import ResponseGoods, ResponseInfoGoods, GoodsInit, ResponseCreateGoods, GoodsUpdate, \
    ResponseUpdateGoods, ResponseDeleteGoods
from pydantic_models.reviews_model import ReviewInit, ResponseCreateReview, ResponseReviews, ReviewInfo, \
    ResponseDeleteReview, ResponseUpdateReview, ReviewUpdate

app = FastAPI()

Base.metadata.create_all(sync_engine, checkfirst=True)


@app.get("/goods")
async def show_goods(offset: int = 0, limit: int = 10) -> ResponseGoods:
    data = await DBgoods.show_goods(offset, limit)
    res = ResponseGoods(status="success", data=data)

    return res


@app.post("/goods")
async def create_goods(goods: GoodsInit) -> ResponseCreateGoods:
    res = await DBgoods.create_goods(goods)
    return res


@app.get("/goods/{goods_id}")
async def info_goods(goods_id: int) -> ResponseInfoGoods:
    data = await DBgoods.info_goods(goods_id)
    res = ResponseInfoGoods(status="success", data=data)
    return res


@app.patch("/goods/{goods_id}")
async def update_goods(goods_id: int, goods: GoodsUpdate) -> ResponseUpdateGoods:
    res = await DBgoods.update_goods(goods_id, goods)
    return res


@app.delete("/goods/{goods_id}")
async def delete_goods(goods_id: int) -> ResponseDeleteGoods:
    res = await DBgoods.delete_goods(goods_id)
    return res


@app.get("/goods/{goods_id}/reviews")
async def show_reviews(goods_id: int, offset: int = 0, limit: int = 10) -> ResponseReviews:
    data = await DBreviews.show_reviews(goods_id, offset, limit)
    res = ResponseReviews(status="success", data=data)
    return res


@app.delete("/goods/{goods_id}/reviews")
async def show_reviews(goods_id: int, offset: int = 0, limit: int = 10) -> ResponseReviews:
    data = await DBreviews.show_reviews(goods_id, offset, limit)
    res = ResponseReviews(status="success", data=data)
    return res


@app.post("/goods/{goods_id}/reviews")
async def create_review(reviews: ReviewInfo, goods_id: int) -> ResponseCreateReview:
    res = await DBreviews.create_review(reviews, goods_id)
    return res


@app.delete("/goods/{goods_id}/reviews")
async def delete_review(goods_id: int, user_id: int) -> ResponseDeleteReview:
    res = await DBreviews.delete_review(goods_id, user_id)
    return res


@app.patch("/goods/{goods_id}/reviews")
async def update_review(goods_id: int, user_id: int, review: ReviewUpdate) -> ResponseUpdateReview:
    res = await DBreviews.update_review(goods_id, user_id, review)
    return res



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
