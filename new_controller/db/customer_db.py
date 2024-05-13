# -*- coding: utf-8 -*-
import bcrypt

from db import main_db


class PostgresDBCustomer(main_db.PostgresDB):
    def __init__(self):
        super().__init__()
        self.KEY_PROFILE = ["customer_name", "phone_number", "email", "birthday", "city", "scores", "customer_img"]
        self.KEY_STR_PROFILE = ", ".join(self.KEY_PROFILE)

        self.KEY_PROFILE_ORDERS = ["goods_id", "customer_name", "city", "delivery_date", "status", "goods_img"]
        self.KEY_STR_PROFILE_ORDERS = ", ".join(self.KEY_PROFILE_ORDERS)

    async def create_review(self, review, goods_id, customer_id):
        error_message = "Ошибка при работе с функцией создания отзыва"

        async with self.connection.acquire() as cursor:
            transaction = cursor.transaction()
            # Начало транзакции
            await transaction.start()
            try:
                # проверяем, что отзыва еще не было
                str_exec = (f"SELECT customer_name"
                            f" from reviews WHERE customer_id = $1 AND goods_id = $2; ")

                info = await cursor.fetchrow(str_exec, customer_id, goods_id)

                if info is not None:
                    res = {
                        "status": "warning",
                        "message": "Вы уже оставляли отзыв на этот товар",
                        "code": 409
                    }
                    await transaction.rollback()
                    return res

                # проверяем, что товар существует
                str_exec = (f"SELECT 1"
                            f" from goods WHERE goods_id = $1; ")

                info = await cursor.fetchrow(str_exec, goods_id)

                if info is None:
                    res = {
                        "status": "error",
                        "message": "Такого товара нет",
                        "code": 404
                    }
                    await transaction.rollback()
                    return res

                # получаем имя пользователя
                str_exec = (f"SELECT customer_name"
                            f" from customers WHERE global_id = $1; ")

                customer_name = await cursor.fetchrow(str_exec, customer_id)
                review["customer_name"] = customer_name[0]
                review["goods_id"] = goods_id
                review["customer_id"] = customer_id

                # загружаем информацию о товара
                keys, values = ", ".join(list(review.keys())), list(review.values())
                str_values = ", ".join([f"${i}" for i in range(1, len(values) + 1)])

                # Записываем
                str_exec = (f'INSERT INTO reviews ({keys}) '
                            f'VALUES ({str_values});')
                await cursor.execute(str_exec, *values)

                await transaction.commit()

                # Отзыв успешно создан
                res = {
                    "status": "success",
                    "message": "Отзыв успешно загружен в базу данных",
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

    async def to_basket(self, goods_id, customer_id):
        error_message = "Ошибка при работе с функцией добавления товара в корзину"

        async with self.connection.acquire() as cursor:
            transaction = cursor.transaction()
            # Начало транзакции
            await transaction.start()
            try:

                # проверяем, что товар существует
                str_exec = (f"SELECT 1"
                            f" from goods WHERE goods_id = $1; ")

                info = await cursor.fetchrow(str_exec, goods_id)

                if info is None:
                    res = {
                        "status": "error",
                        "message": "Такого товара нет",
                        "code": 404
                    }
                    await transaction.rollback()
                    return res

                goods_id = '{"' + str(goods_id) + '"}'
                str_exec = ("UPDATE customers "
                            f"SET basket = jsonb_set(basket, '{goods_id}', '1', true) "
                            f"WHERE global_id = $1;")

                # Записываем
                await cursor.execute(str_exec, customer_id)

                await transaction.commit()

                # Отзыв успешно создан
                res = {
                    "status": "success",
                    "message": "Товар успешно добавлен в корзину",
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

    async def show_profile(self, customer_id):
        # Пользователь хочет посмотреть свой профиль
        error_message = "Ошибка при работе с функцией просмотра профиля"
        res = dict()

        async with self.connection.acquire() as cursor:
            try:

                # Выгружаем всю информацию из профиля
                str_exec = (f"SELECT  {self.KEY_STR_PROFILE}"
                            f" from customers WHERE global_id = $1; ")

                profile_info = await cursor.fetchrow(str_exec, customer_id)
                profile_info = dict(zip(self.KEY_PROFILE, profile_info))

                date_string = profile_info.get("birthday", None)

                # переводим в нормальное значение дату
                if date_string is not None:
                    profile_info["birthday"] = date_string.strftime("%Y-%m-%d")

                # Выгружаем всю информацию о заказах
                str_exec = (f"SELECT  {self.KEY_STR_PROFILE_ORDERS}"
                            f" from orders WHERE customer_id = $1; ")

                all_orders = await cursor.fetch(str_exec, customer_id)

                # переводим в удобную дату
                for d in all_orders:
                    d = dict(zip(self.KEY_PROFILE_ORDERS, d))
                    if 'delivery_date' in d:
                        d['delivery_date'] = d['delivery_date'].strftime("%Y-%m-%d")

                profile_info["orders"] = all_orders
                # если все хорошо
                res = {'status': "success",
                       'data': profile_info,
                       "code": 200}

            except Exception as error:
                print(error)
                res = {'status': "error",
                       'data': error_message,
                       "code": 500}

            finally:
                return res
