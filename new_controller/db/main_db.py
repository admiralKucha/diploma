import asyncpg


class PostgresDB:
    def __init__(self):
        self.connection = None
        self.user = "postgres"
        self.password = "postgres"
        self.host = "localhost"
        self.port = "5432"
        self.database = "diploma"
        self.connection = None

        self.KEY_CHECKER = ["id", "username", "user_group", "is_banned"]
        self.KEY_STR_CHECKER = ", ".join(self.KEY_CHECKER)

    async def create_pool(self):
        self.connection = await asyncpg.create_pool(user=self.user,
                                                    password=self.password,
                                                    host=self.host,
                                                    port=self.port,
                                                    database=self.database,
                                                    min_size=5,
                                                    max_size=5,
                                                    )

    async def check_email(self, email, cursor):
        # Функция проверяет уникальность почты
        res = dict()
        try:

            # проверка на уникальность почты
            str_exec = f"SELECT global_id FROM all_users WHERE username = $1;"
            global_id = await cursor.fetchrow(str_exec, email)

            if global_id is not None:
                res = {
                    "status": False,
                    "data": "Ошибка при работе с добавлением пользователя"
                            "(пользователь с такой почтой уже существует)"
                }
                return res

            # Все хорошо
            res = {
                "status": True,
                "message": "Почта уникальна"
            }

        except Exception as error:
            print(error)
            res['status'] = False

        finally:
            return res






