# -*- coding: utf-8 -*-
import bcrypt

from db import main_db


class PostgresDBAdmin(main_db.PostgresDB):

    async def create_new_goods(self, goods):
        error_message = "Ошибка при работе с функцией создания товара"

        async with self.connection.acquire() as cursor:
            transaction = cursor.transaction()
            # Начало транзакции
            await transaction.start()
            try:

                # загружаем информацию о товара
                keys, values = ", ".join(list(goods.keys())), list(goods.values())
                str_values = ", ".join([f"${i}" for i in range(1, len(values) + 1)])

                # Записываем
                str_exec = (f'INSERT INTO goods ({keys}) '
                            f'VALUES ({str_values});')
                await cursor.execute(str_exec, *values)

                await transaction.commit()

                # Товар успешно создан
                res = {
                        "status": "success",
                        "message": "Товар успешно загружен в базу данных",
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
