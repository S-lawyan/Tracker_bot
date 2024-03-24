import asyncio
import json
import re

from aiohttp import ClientSession, ClientConnectionError
from async_timeout import timeout
from loguru import logger
from bot.utils.exceptions import (
    WildberriesAPIGetProductTimeout,
    WildberriesAPIClientConnectionError,
    WildberriesAPIUncorrectedQuery,
    WildberriesAPIProductNotFound,
)
from bot.utils.models import Product


class WildberriesAPI:
    def __init__(self, http_session_maker):
        self.session: ClientSession = http_session_maker()

    async def get_product(self, query: str) -> Product:
        # Выделение артикула
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
        if not json_response["data"]["products"]:
            logger.error(f"Товар не найден:\n{query}")
            raise WildberriesAPIProductNotFound()
        return wb_pars_product(product=json_response["data"]["products"][0])


async def preprocess_query(query: str) -> int:
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


async def get_product_response(session: ClientSession, article: int) -> str:
    request_ulr: str = "https://card.wb.ru/cards/v2/detail"
    params = {
        "appType": 1,
        "curr": "rub",
        "dest": -1257786,
        "spp": 30,
        "nm": article
    }

    async with session.get(url=request_ulr, params=params) as response:
        return await response.text(encoding='utf-8')


def wb_pars_product(product: dict) -> Product:
    return Product(
        article=product.get("id", 0),
        name=product.get("name", ""),
        brand=product.get("brand", ""),
        colors=', '.join(color["name"] for color in product.get("colors", [])),
        price=get_price(sizes=product["sizes"][0]),
        count=get_count(sizes=product["sizes"][0].get("stocks", 0)),
        supplier=product.get("supplier", ""),
        supplier_id=product.get("supplierId", 0)
        # review_rating=product.get("reviewRating", 0),
        # feedbacks=product.get("feedbacks", 0),
        # supplier_rating=product.get("supplierRating", 0)
    )


def get_price(sizes: dict) -> int:
    if sizes.get("price", None):
        return int(sizes["price"]["total"]/100)
    else:
        return 0


def get_count(sizes: list) -> int:
    return sum(int(i["qty"]) for i in sizes)
