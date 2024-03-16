import asyncio
import json
import re

from aiohttp import ClientSession, ClientConnectionError
from async_timeout import timeout
from loguru import logger
from api.exceptions import (
    WildberriesAPIGetProductTimeout,
    WildberriesAPIClientConnectionError,
    WildberriesAPIPreprocessArticleError,
    WildberriesAPIUncorrectedQuery,
)
from api.models import Product


class WildberriesAPI:
    def __init__(self, http_session_maker):
        self.session: ClientSession = http_session_maker()

    async def get_product(self, query: str):
        # Выделение артикула
        # TODO учесть исключения этой функции в ответе пользователю
        article: int = await preprocess_query(query=query)
        # Выполнения запроса, получение товара
        try:
            async with timeout(10):
                response = await get_product_response(session=self.session, article=article)
        except asyncio.Timeout:
            logger.error(f"Запрос товара вылетел по таймауту:\n{query}")
            raise WildberriesAPIGetProductTimeout()
        except ClientConnectionError as exc:
            logger.error(f"Ошибка подключение HTTP-сессии:\n{exc}")
            raise WildberriesAPIClientConnectionError()
        json_response = json.loads(response)
        if "????" in response:
            logger.error(f"Если запросили несуществующий товар, артикула которого нет в магазине")
            raise ...
        elif json_response["какая-то дата"] == ["пустая"]:
            logger.error(f"Если вернулась какая-то другая ошибка")
            raise ...
        return pars_product(response=json_response)


async def preprocess_query(query: str) -> int:
    try:
        # Проверка query на соответствие артикулу
        if re.match(r'^\d+$', query):
            return int(query)
        # Проверка query на соответствие ссылки с артикулом
        elif re.match(r'^https?://www\.wildberries\.ru/catalog/\d+', query):
            match = re.search(r'\d+', query)  # Извлекаем артикул из ссылки
            if match:
                return int(match.group())
        else:
            logger.error(f"Некорректный запрос товара:\n{query}")
            raise WildberriesAPIUncorrectedQuery()
            # TODO сделать обработку этого исключения в ответе пользователю:
            #  это не похоже на артикул или ссылку на товар
    except Exception as exc:
        logger.error(f"Ошибка предобработки артикула:\n{exc}")
        raise WildberriesAPIPreprocessArticleError()
        # TODO сделать обработку этого исключения в ответе пользователю:
        #  Предложение попробовать снова


async def get_product_response(session: ClientSession, article: int) -> str:
    # request_url: str = "https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm=67858518"
    request_ulr: str = "https://card.wb.ru/cards/v2/detail"
    params = {
        "appType": 1,
        "curr": "rub",
        "dest": -1257786,
        "spp": 30,
        "nm": article
    }

    async with session.get(url=request_ulr, params=params) as response:
        return await response.text()


async def pars_product(response: dict) -> Product:
    product = Product(
        name = response[""],
        price = response[""],
        count = response[""],
        review_rating = response[""],
        feedbacks = response[""]
        # supplier_rating = response[""]
    )
    return product

