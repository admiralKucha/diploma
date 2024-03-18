from fastapi import APIRouter
from pydantic_models.seller_model import SellerInit, ResponseCreateSeller
import db.admin as DBadmin

admin = APIRouter(prefix="/admin")


@admin.post("/seller", tags=["Администратор"])
async def admin_create_seller(seller: SellerInit) -> ResponseCreateSeller:
    res = await DBadmin.create_seller(seller)
    return res



