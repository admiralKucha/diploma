# -*- coding: utf-8 -*-
import random
import string
from email.message import EmailMessage
from random import choice
from aiosmtplib import SMTP

import bcrypt

from db import main_db


class PostgresDBGuest(main_db.PostgresDB):
    def __init__(self):
        super().__init__()
        self.KEY_AUTH = ["global_id", "username", "password", "user_group"]
        self.KEY_STR_AUTH = ", ".join(self.KEY_AUTH)

        self.KEY_ARTICLE_ALL = ["article_id", "article_title"]

        self.KEY_ARTICLE_ID = ["article_id", "article_title", "article_small_info", "article_text"]
        self.KEY_STR_ARTICLE_ID = ", ".join(self.KEY_ARTICLE_ID)

    async def authentication_user(self, user: dict):
        error_message = "Ошибка при работе с функцией входа пользователя в учетную запись"
        res = dict()
        username, password = user["username"], user["password"]

        async with self.connection.acquire() as cursor:
            try:
                # Берем информацию по логину
                str_exec = (f"SELECT {self.KEY_STR_AUTH} FROM all_users"
                            f" WHERE username = $1")
                res_temp = await cursor.fetchrow(str_exec, username)

                # Логина нет
                if res_temp is None:
                    res = {
                        "status": "error",
                        "message": "Такого логина не существует",
                        "code": 403
                    }
                    return

                # Группируем информацию
                buf = dict(zip(self.KEY_AUTH, res_temp))
                real_password = buf.pop("password")

                # Проверяем пароль
                if not bcrypt.checkpw(password.encode('utf-8'), real_password.encode('utf-8')):

                    # Пароль неверный
                    res = {
                        "status": "error",
                        "message": "Неверный пароль",
                        "code": 401
                    }
                    return res

                # если все хорошо
                res = {
                    "status": "success",
                    "message": "Пользователь авторизован",
                    "id": buf['global_id'],
                    "user_group": buf["user_group"],
                    "code": 200
                }

            except Exception as error:
                print(error)
                res = {
                    "status": "error",
                    "message": error_message,
                    "code": 500
                }

            finally:
                return res

    async def add_user(self, email, password, cursor):
        error_message = "Ошибка при работе с функцией создания логина и пароля покупателя"
        res = dict()
        try:
            # Создаем пароль пользователю
            salt = bcrypt.gensalt(rounds=10)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

            # Вставляем пароль
            str_exec = (f"INSERT INTO all_users (username, password, user_group) VALUES"
                        f" ($1, $2, '1') RETURNING username, password, global_id;")

            _login = await cursor.fetchrow(str_exec, email, hashed_password)

            # Запись не вставилась
            if _login is None:
                res = {
                    "status": False,
                    "message": error_message,
                    "data": "Ошибка сервера"
                }

            # все получилось
            res = {
                'status': True,
                'data': {
                    "username": _login[0],
                    "password": password,
                    "id": _login[2]
                }
            }

        except Exception as error:
            print(error)
            res = {
                "status": False,
                "message": error_message,
            }

        finally:
            return res

    async def make_new_form(self, customer, customer_id, cursor):

        error_message = "Ошибка при работе с добавлением анкеты(make_new_form)"
        res = dict()
        try:
            customer = customer.model_dump()
            customer.pop("password")
            keys, values = ", ".join(list(customer.keys())), list(customer.values())
            str_values = ", ".join([f"${i}" for i in range(2, len(values) + 2)])

            # Записываем
            str_exec = (f'INSERT INTO customers ({keys}, global_id) '
                        f'VALUES ({str_values}, $1);')
            await cursor.execute(str_exec, customer_id, *values)

            res = {"status": True}

        except Exception as error:
            print(error)
            res = {
                "status": False,
                "message": error_message,
            }

        finally:
            return res

    async def create_new_customer(self, customer):
        error_message = "Ошибка при работе с функцией создания пользователя"
        res_temp = dict()
        res = dict()
        res_temp['status'] = True
        res['status'] = "success"

        async with self.connection.acquire() as cursor:
            transaction = cursor.transaction()
            # Начало транзакции
            await transaction.start()
            try:

                email = customer.email
                password = customer.password
                # Проверяем уникальность почты
                res_temp = await self.check_email(email, cursor=cursor)
                if not res_temp['status']:
                    res = {
                        "status": "error",
                        "message": error_message,
                        "data": res_temp["data"],
                        "code": 409
                    }
                    await transaction.rollback()
                    return res

                # Создаем логин и пароль
                _login: dict[str, str | dict] = await self.add_user(email, password, cursor)
                # не смогли создать логин-пароль
                if not _login['status']:
                    res = {
                        "status": "error",
                        "message": error_message,
                        "data": "Не получилось создать логин-пароль для пользователя",
                        "code": 500
                    }
                    await transaction.rollback()
                    return res

                student_id = _login['data'].pop("id")

                # загружаем основную информацию о пользователе
                res = await self.make_new_form(customer, student_id, cursor)
                if not res['status']:
                    res = {
                        "status": "error",
                        "message": error_message,
                        "data": res.get("data", "Не получилось загрузить информацию о пользователе"),
                        "code": 500
                    }
                    await transaction.rollback()
                    return

                # Отправляем письмо
                _hash = ''.join(random.choices(string.ascii_letters + string.digits, k=30))

                msg = EmailMessage()
                msg.set_content(f"Здравствуйте, {customer.customer_name}!\n\nВы успешно зарегистрировали аккаунт. Спасибо за использование нашего сервиса.")

                msg['Subject'] = 'Регистрация аккаунта'
                msg['From'] = 'test_tvgu_24@mail.ru'
                msg['To'] = 'glin.maxim@yandex.ru'

                async with SMTP(hostname="smtp.mail.ru", port=465, use_tls=True) as smtp:
                    await smtp.login("test_tvgu_24@mail.ru", "Swvev46pAARiytbp0hLZ")
                    await smtp.send_message(msg)

                await transaction.commit()
                # Пользователь успешно создан
                res = {
                        "status": "success",
                        "message": "Пользователь добавлен в систему",
                        "code": 201
                }

            except Exception as error:
                print(error)
                res = {
                    "status": "error",
                    "message": error_message,
                    "code": 500
                }
                await transaction.rollback()

            finally:
                return res

    async def show_all_article(self):
        # Пользователь хочет посмотреть какие есть статьи
        error_message = "Ошибка при работе с функцией просмотра статей"
        res = dict()

        async with self.connection.acquire() as cursor:
            try:

                # Выгружаем id - название. Проверка - видимость
                str_exec = (f"SELECT article_id, article_title "
                            f"from articles WHERE is_visible = True; ")

                all_articles = await cursor.fetch(str_exec)

                all_articles = [dict(zip(self.KEY_ARTICLE_ALL, values)) for values in all_articles]
                # если все хорошо
                res = {'status': "success",
                       'data': all_articles,
                       "code": 200}

            except Exception as error:
                print(error)
                res = {'status': "error",
                       'data': error_message,
                       "code": 500}

            finally:
                return res

    async def show_id_article(self, article_id):
        # Пользователь хочет посмотреть определенную статью
        error_message = "Ошибка при работе с функцией просмотра определенной статьи"
        res = dict()

        async with self.connection.acquire() as cursor:
            try:
                # Выгружаем id - название. Проверка - видимость
                str_exec = (f"SELECT  {self.KEY_STR_ARTICLE_ID}"
                            f" from articles WHERE is_visible = True AND article_id = $1; ")

                article_info = await cursor.fetchrow(str_exec, article_id)

                if article_info is None:
                    res = {"status": "warning",
                           'message': "Такой статьи нет",
                           "code": 404}
                    return res

                all_articles = dict(zip(self.KEY_ARTICLE_ID, article_info))
                # если все хорошо
                res = {'status': "success",
                       'data': all_articles,
                       "code": 200}

            except Exception as error:
                print(error)
                res = {'status': "error",
                       'data': error_message,
                       "code": 500}

            finally:
                return res








