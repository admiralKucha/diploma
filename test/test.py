import asyncio
import time
from inspect import get_annotations
import aiohttp


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()


async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(url, session) for url in urls]
        return await asyncio.gather(*tasks)


async def main():
    start = time.time()
    urls = []
    for i in range(0, 1):
        urls.append(f'http://127.0.0.1:8000/goods/?offset={i}&limit=10')
    start = time.time()
    responses = await fetch_all(urls)
    print(time.time() - start, "Конец")
    end = time.time() - start
    print(10000/end, "В секунду")
    print(end / 10000, "Время одного запроса в среднем")
    # Обработка ответов


class Test:
    a: int
    b: int


if __name__ == "__main__":
    #asyncio.run(main())
    a: int = "fsdf"
    print(get_annotations(Test))
