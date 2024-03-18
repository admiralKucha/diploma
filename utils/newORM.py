from pydantic import BaseModel
from sqlalchemy import select, insert


def obj_fetchone(result, obj):
    res = result.fetchone()
    if res is None:
        return res
    keys = obj.__annotations__.keys()
    res = obj(**dict(zip(keys, res)))
    return res


def obj_fetchall(result, obj):
    res = result.all()
    keys = obj.__annotations__.keys()
    res = [obj(**dict(zip(keys, goods))) for goods in res]
    return res


def obj_select(tablename, obj):
    keys = [getattr(tablename, el) for el in obj.__annotations__.keys()]
    print(keys)
    return select(*keys)


def obj_insert(tablename, obj: list[BaseModel]):
    array_values = [el.model_dump() for el in obj]
    return insert(tablename), array_values

