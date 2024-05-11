from fastapi import APIRouter

from db import main_db
from db import guest_db

main_base = main_db.PostgresDB()
databaseGuest = guest_db.PostgresDBGuest()

router = APIRouter()


@router.on_event("startup")
async def startup():
    await databaseGuest.create_pool()
    await main_base.create_pool()
