import asyncio

from api.http_session import HttpSessionMaker
from bot.services import storage
from bot.services import bot
from api.wb_adapter import WildberriesAPI
from loguru import logger
from bot.utils import utilities as utl
from bot.utils.models import Product
from bot.utils.exceptions import (
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
                await asyncio.sleep(0.25)
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
        logger.info(f"Артикул товара больше не действителен. Оповещение пользователя об этом.")
        for user in tracking_users:
            await bot.send_message(
                chat_id=user,
                text=utl.wb_alert_user_about_not_found(
                    old_product=old_product
                )
            )
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

    # Проверка наличия товара
    if new_count != 0:
        # Товар в наличии
        if old_count == 0:
            # Если его до этого не было
            for user in tracking_users:
                await bot.send_message(
                    chat_id=user,
                    text=utl.wb_alert_user_about_in_stock(
                        product=new_product
                    )
                )
        else:
            # Если до этого был
            if new_price <= old_price * 0.9:
                # Если цена изменилась достаточно
                for user in tracking_users:
                    await bot.send_message(
                        chat_id=user,
                        text=utl.wb_alert_user_about_lowed_price(
                            new_product=new_product,
                            old_product=old_product
                        )
                    )
            else:
                # Если цена не изменилась, возросла или уменьшилась недостаточно
                return
    else:
        if new_count == 0 and old_count != 0:
            # Товар был до этого, но сейчас пропал из наличия
            for user in tracking_users:
                await bot.send_message(
                    chat_id=user,
                    text=utl.wb_alert_user_about_out_stock(
                        product=new_product
                    )
                )
        else:
            logger.info("Событие требующее внмания")
