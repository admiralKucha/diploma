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
                res = {
                    "status": "error",
                    "message": error_message,
                    "code": 500
                }
                await transaction.rollback()

            finally:
                return res

    async def change_goods(self, goods, goods_id):
        error_message = "Ошибка при работе с функцией изменения товара"

        async with self.connection.acquire() as cursor:
            transaction = cursor.transaction()
            # Начало транзакции
            await transaction.start()
            try:

                # загружаем информацию о товара
                keys, values = ", ".join(list(goods.keys())), list(goods.values())
                str_values = ", ".join([f"${i}" for i in range(3, len(values) + 3)])

                # Записываем
                str_exec = (f'UPDATE goods SET ({keys}, goods_id) ='
                            f' ({str_values}, $1) '
                            f'WHERE goods_id = $2 RETURNING goods_id;')
                res = await cursor.fetchrow(str_exec, goods_id, goods_id, *values)

                if res is None:
                    res = {
                        "status": "error",
                        "message": "Такого товара нет",
                        "code": 404
                    }
                    await transaction.rollback()
                    return res

                await transaction.commit()

                # Товар успешно создан
                res = {
                    "status": "success",
                    "message": "Информация о товаре изменена",
                    "code": 201
                }

            except Exception as error:
                res = {
                    "status": "error",
                    "message": error_message,
                    "code": 500
                }
                await transaction.rollback()

            finally:
                return res

    async def delete_goods(self, goods_id):
        # Администратор удаляет товар
        res = dict()

        async with self.connection.acquire() as cursor:
            try:
                transaction = cursor.transaction()
                # Начало транзакции
                await transaction.start()

                # Удаляем товар
                str_exec = (f"DELETE FROM goods "
                            f"WHERE goods_id = $1 "
                            f"RETURNING goods_id;")
                info_goods = await cursor.fetchrow(str_exec, goods_id)

                # Такого товара нет?
                if info_goods is None:
                    res = {"status": "warning",
                           'message': "Такого товара нет",
                           "code": 404}
                    await transaction.rollback()
                    return res

                # Сохраняем результат
                await transaction.commit()
                res = {"status": "success",
                       'message': "Товар удален",
                       "code": 202}

            except (Exception) as error:
                print(error)
                await transaction.rollback()
                res = {"status": "error",
                       'message': "Ошибка при работе с функцией удалением товара",
                       "code": 500}

            finally:
                return res

    async def create_new_article(self, article):
        error_message = "Ошибка при работе с функцией создания статьи"

        async with self.connection.acquire() as cursor:
            transaction = cursor.transaction()
            # Начало транзакции
            await transaction.start()
            try:

                # Проверяем, есть ли такая статья

                str_exec = f'SELECT article_id FROM articles WHERE article_title = $1;'

                info_article = await cursor.fetchrow(str_exec, article["article_title"])

                # Такая статья уже есть?
                if info_article is not None:
                    res = {"status": "warning",
                           'message': "Такая статья уже есть",
                           "code": 409}
                    await transaction.rollback()
                    return res

                # загружаем информацию о статье
                keys, values = ", ".join(list(article.keys())), list(article.values())
                str_values = ", ".join([f"${i}" for i in range(1, len(values) + 1)])

                # Записываем
                str_exec = (f'INSERT INTO articles ({keys}) '
                            f'VALUES ({str_values});')
                await cursor.execute(str_exec, *values)

                await transaction.commit()

                # Товар успешно создан
                res = {
                    "status": "success",
                    "message": "Статья успешно загружена в базу данных",
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

    async def change_article(self, article, article_id):
        error_message = "Ошибка при работе с функцией изменения статьи"

        async with self.connection.acquire() as cursor:
            transaction = cursor.transaction()
            # Начало транзакции
            await transaction.start()
            try:

                # загружаем информацию о статье
                keys, values = ", ".join(list(article.keys())), list(article.values())
                str_values = ", ".join([f"${i}" for i in range(3, len(values) + 3)])

                # Записываем
                str_exec = (f'UPDATE articles SET ({keys}, article_id) ='
                            f' ({str_values}, $1) '
                            f'WHERE article_id = $2 RETURNING article_id;')
                res = await cursor.fetchrow(str_exec, article_id, article_id, *values)

                if res is None:
                    res = {
                        "status": "error",
                        "message": "Такой статьи нет",
                        "code": 404
                    }
                    await transaction.rollback()
                    return res

                await transaction.commit()

                # Статья успешно изменена
                res = {
                    "status": "success",
                    "message": "Информация о статье изменена",
                    "code": 201
                }

            except Exception as error:
                res = {
                    "status": "error",
                    "message": error_message,
                    "code": 500
                }
                await transaction.rollback()

            finally:
                return res

    async def delete_article(self, goods_id):
        # Администратор удаляет статью
        res = dict()

        async with self.connection.acquire() as cursor:
            try:
                transaction = cursor.transaction()
                # Начало транзакции
                await transaction.start()

                # Удаляем товар
                str_exec = (f"DELETE FROM articles "
                            f"WHERE article_id = $1 "
                            f"RETURNING article_id;")
                info_article = await cursor.fetchrow(str_exec, goods_id)

                # Такой статьи нет?
                if info_article is None:
                    res = {"status": "warning",
                           'message': "Такой статьи нет",
                           "code": 404}
                    await transaction.rollback()
                    return res

                # Сохраняем результат
                await transaction.commit()
                res = {"status": "success",
                       'message': "Статья удалена",
                       "code": 202}

            except (Exception) as error:
                print(error)
                await transaction.rollback()
                res = {"status": "error",
                       'message': "Ошибка при работе с функцией удаления статьи",
                       "code": 500}

            finally:
                return res
