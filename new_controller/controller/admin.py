from fastapi import APIRouter, Response, Cookie


admin = APIRouter(prefix="")


@admin.post("/goods", tags=["Админ"], summary="Создать товар")
async def create_goods():
    pass
    return 212


@admin.post("/goods/{goods_id}", tags=["Админ"], summary="Изменить определенный товар")
async def change_goods(goods_id: int):
    pass
    return 212


@admin.delete("/goods/{goods_id}", tags=["Админ"], summary="Удалить товар")
async def delete_goods(goods_id: int):
    pass
    return 212


@admin.post("/articles", tags=["Админ"], summary="Создать статьи")
async def create_article():
    pass
    return 212


@admin.delete("/articles/{article_id}", tags=["Админ"], summary="Изменить статью")
async def delete_article(article_id: int):
    pass
    return 212


@admin.get("/stats", tags=["Админ"], summary="Посмотреть статистику сайта")
async def show_stats():
    pass
    return 212