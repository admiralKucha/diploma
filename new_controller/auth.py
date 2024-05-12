import json
from functools import wraps

from cryptography.fernet import Fernet, InvalidToken
from fastapi import Response
from init import main_base


cipher_suite = Fernet(Fernet.generate_key())


def logout_check(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session: str | None = kwargs.get("session", None)
        if session is None:
            res = {"status": "error", "message": "Пользователь не был в аккаунте"}
            res = Response(content=json.dumps(res, ensure_ascii=False), status_code=401, media_type='application/json')
            res.delete_cookie("session")

            res.delete_cookie("role")
            return res

        try:
            _id = int(cipher_suite.decrypt(session))
        except InvalidToken:
            # не наш токен
            res = {"status": "error", "message": "Пользователь не был в аккаунте"}
            res = Response(content=json.dumps(res, ensure_ascii=False), status_code=401, media_type='application/json')
            res.delete_cookie("session")
            res.delete_cookie("role")
            return res

        if await main_base.checker(_id) is None:
            res = {"status": "error", "message": "Пользователь не был в аккаунте"}
            res = Response(content=json.dumps(res, ensure_ascii=False), status_code=401, media_type='application/json')
            res.delete_cookie("session")
            res.delete_cookie("role")
            return res

        return await func(*args, **kwargs)

    return wrapper


def anonymous(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session: str | None = kwargs.get("session", None)
        if session is not None:
            try:
                _id = int(cipher_suite.decrypt(session))
            except InvalidToken:
                # не наш токен
                return await func(*args, **kwargs)

            res = {"status": "warning", "message": "Пользователь уже авторизован"}
            return Response(content=json.dumps(res, ensure_ascii=False), status_code=403, media_type='application/json')

        return await func(*args, **kwargs)

    return wrapper


def admin_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session: str | None = kwargs.get("session", None)
        if session is None:
            res = {"status": "error", "message": "Необходимо пройти авторизацию"}
            return Response(content=json.dumps(res, ensure_ascii=False), status_code=401, media_type='application/json')

        try:
            _id = int(cipher_suite.decrypt(session))
        except InvalidToken:
            # не наш токен
            res = {"status": "error", "message": "Необходимо заново пройти авторизацию"}
            res = Response(content=json.dumps(res, ensure_ascii=False), status_code=401, media_type='application/json')
            res.delete_cookie("session")

            return res

        user = await main_base.checker(_id)
        if user is None:
            res = {"status": "error", "message": "Необходимо заново пройти авторизацию"}
            res = Response(content=json.dumps(res, ensure_ascii=False), status_code=401, media_type='application/json')
            res.delete_cookie("session")

            return res

        if user.user_group != 0 and user.user_group != 4:
            res = {"status": "error", "message": "Недостаточно прав"}
            return Response(content=json.dumps(res, ensure_ascii=False), status_code=403, media_type='application/json')

        if user.is_banned is True:
            res = {"status": "error", "message": "Пользователь заблокирован"}
            res = Response(content=json.dumps(res, ensure_ascii=False), status_code=403, media_type='application/json')
            res.delete_cookie("session")

            return res

        kwargs["session"] = user.id
        return await func(*args, **kwargs)

    return wrapper


def customer_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):

        # нет куки
        session: str | None = kwargs.get("session", None)

        if session is None:
            res = {"status": "error", "message": "Необходимо пройти авторизацию"}
            return Response(content=json.dumps(res, ensure_ascii=False), status_code=401, media_type='application/json')

        try:
            _id = int(cipher_suite.decrypt(session))
        except InvalidToken:
            # не наш токен
            res = {"status": "error", "message": "Необходимо заново пройти авторизацию"}
            res = Response(content=json.dumps(res, ensure_ascii=False), status_code=401, media_type='application/json')
            res.delete_cookie("session")

            return res

        user = await main_base.checker(_id)

        # не нашли такого пользователя
        if user is None:
            res = {"status": "error", "message": "Необходимо заново пройти авторизацию"}
            res = Response(content=json.dumps(res, ensure_ascii=False), status_code=401, media_type='application/json')
            res.delete_cookie("session")

            return res

        # неправильная роль
        if user.user_group != 1:
            res = {"status": "error", "message": "Недостаточно прав"}
            return Response(content=json.dumps(res, ensure_ascii=False), status_code=403, media_type='application/json')

        # сохраняем для запроса далее id пользователя
        kwargs["session"] = user.global_id
        return await func(*args, **kwargs)

    return wrapper
