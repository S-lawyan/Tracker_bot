from api.http_session import HttpSessionMaker
from bot.services import storage
from api.wb_adapter import WildberriesAPI
from loguru import logger
import json
from bot.utils.models import Product
from bot.utils.exceptions import (
    DatabaseExecuteQueryError,
    WildberriesAPIProductNotFound,
    WildberriesAPIGetProductTimeout,
    WildberriesAPIClientConnectionError,
)


class WildberriesTracker:
    def __init__(self, http_session_maker: HttpSessionMaker):
        self.http_session_maker = http_session_maker

    async def tracking(self):
        api: WildberriesAPI = WildberriesAPI(self.http_session_maker)
        # TODO сделать проверку для каждого пользователя индивидуально...
        #  Как у нас в префекте когда асинхронно выполняется список.
        #  А для реализации настроек для отдельного пользователя сделать выгрузку их из БД в отдельный класс
        #  по пулу айдишников в виде параметра функции выгрузки.
        #  Таким образом для каждого пуля пользователей при распараллеливании получится
        #  свой класс с сеттингами для обработки продуктов.
        products_poll: dict = await storage.get_all_products()
        if products_poll == {}:
            logger.info("Товаров для отслеживания нет")
            return
        else:
            for article in products_poll:
                # TODO Сюда передавать сеттинги пользователя
                product_data: Product = products_poll[article]["data"]
                tracking_users: list = products_poll[article]["users"]
                await update_product(api=api, old_product=product_data, tracking_users=tracking_users)
            logger.info(f"Проверка товаров завершена.")

async def update_product(
        api: WildberriesAPI,
        old_product: Product,
        tracking_users: list
) -> None:
    try:
        new_product: Product = await api.get_product(query=str(old_product.article))
    except (
            WildberriesAPIGetProductTimeout,
            WildberriesAPIClientConnectionError,
    ) as exc:
        logger.info(f"Ошибка WildberriesAPI при получении старого билета во время проверки цен\n{exc}")
        return
    except WildberriesAPIProductNotFound:
        logger.info(f"Товар пропал с сайта или его артикул изменился. Оповещение пользователю.")
        # TODO в идеале сюда передать экземпляр класса бота чтобы отправить алерт
        return
    await search_changes(
        old_product=old_product,
        new_product=new_product,
        tracking_users=tracking_users
    )


async def search_changes(
    old_product: Product,
    new_product: Product,
    tracking_users: list
) -> None:
    old_price: int = old_product.total_price
    # new_price: int = new_product.total_price
    new_price: float = old_product.total_price * 0.9
    old_count: int = old_product.count
    new_count: int = new_product.count
    # TODO сюда передавать процент из сеттинга
    # if (new_price <= old_price * 0.9) and (new_count != old_count)
    if new_price <= old_price * 0.9:
        # Изменилась только цена
        pass
    else:
        logger.info(f"Для продукта {old_product.article} изменилась цена с {old_product.total_price} на {new_product.total_price}")
        return

