import json

from fastapi import APIRouter, Response, Cookie
from auth import cipher_suite, anonymous
from init import databaseGuest

from models.user import UserAuth

from models.customer import CustomerInit

from auth import customer_required

_user = APIRouter(prefix="")


@_user.post("/authentication", tags=["Юзер"], summary="Авторизоваться")
@anonymous
async def authentication(user: UserAuth, session: str = Cookie(default=None, include_in_schema=False)):
    # авторизация
    res = await databaseGuest.authentication_user(user.dict())  # узнали, есть ли человек и забанен ли он
    code = res.pop("code")

    if res['status'] != "error":
        # пользователь прошел авторизацию
        user_id, role = res.pop('id'), res.pop("user_group")
        response = Response(content=json.dumps(res, ensure_ascii=False), status_code=code,
                            media_type='application/json', headers={"Accept": "application/json"})

        # добавляем cookie
        response.set_cookie("session", cipher_suite.encrypt(str(user_id).encode()).decode())

        return response
    else:
        # пользователь не прошел авторизацию, удаляем старые cookie, если есть
        res = Response(content=json.dumps(res, ensure_ascii=False), status_code=code,
                       media_type='application/json', headers={"Accept": "application/json"})
        res.delete_cookie("session")

        return res


@_user.post("/logout", tags=["Юзер"], summary="Выйти из аккаунта")
@customer_required
async def logout_user(session: str = Cookie(default=None, include_in_schema=False)):
    pass
    return 212


@_user.post("/registration", tags=["Юзер"], status_code=201, summary="Создание нового аккаунта")  # регистрация
@anonymous
async def registration(customer: CustomerInit, session: str = Cookie(default=None, include_in_schema=False)):
    # Сохраняем данные нового пользователя
    res = await databaseGuest.create_new_customer(customer)
    code = res.pop("code")

    return Response(content=json.dumps(res, ensure_ascii=False), status_code=code,
                    media_type='application/json', headers={"Accept": "application/json"})
