
from aiogram import types
from aiogram.dispatcher.filters import Text
from bot.keyboards.client_kb import *
from bot.services import dp
from bot.services import wb
from bot.services import storage
from bot.filters.is_admin import IsAdmin
from bot.utils.models import Product
from bot.utils import utilities as utl
from bot.utils.exceptions import (
    WildberriesAPIGetProductTimeout,
    WildberriesAPIClientConnectionError,
    WildberriesAPIUncorrectedQuery,
    WildberriesAPIProductNotFound,
    DatabaseExecuteQueryError
)


# ================= БЛОК ОСНОВНЫХ КОМАНД БОТА ==============================
@dp.message_handler(IsAdmin(), commands=["start"], state=None)
@dp.message_handler(IsAdmin(), Text(startswith="меню", ignore_case=True), state='*')
@dp.message_handler(IsAdmin(), Text(startswith="главное меню", ignore_case=True), state='*')
async def command_start(message: types.Message) -> None:
    if await storage.check_user(user_id=int(message.from_user.id)):
        await message.answer(text="Меню администратора", reply_markup=admin_panel_main)
    else:
        await storage.insert_user(user_id=int(message.from_user.id))
        await message.answer(
            text=f"Привет, {message.from_user.first_name}! 👋\n\n"
                 f"Сейчас для тебя выставлены стандартный настройки:\n"
                 f"<b>Порог разницы цен</b> - 10%\n"
                 f"\n"
                 f"Как изменить настройки - описано в /help",
            reply_markup=admin_panel_main
        )


@dp.message_handler(IsAdmin(), commands=["help"], state='*')
@dp.message_handler(IsAdmin(), Text(startswith="помощь", ignore_case=True), state='*')
async def command_help_message(message: types.Message) -> None:
    await message.answer(text="help")


@dp.message_handler(IsAdmin(), content_types=['text'], state='*')
async def get_query(message: types.Message):
    query: str = message.text
    try:
        product: Product = await wb.get_product(query=query)
        await storage.insert_product(product=product, user_id=int(message.from_user.id))
        await message.answer(text=utl.wb_create_product_message(product=product), reply_markup=None)
    except (
            WildberriesAPIGetProductTimeout,
            WildberriesAPIClientConnectionError,
    ):
        await message.answer(text="❌ Произошла ошибка, повторите попытку")
    except WildberriesAPIProductNotFound:
        await message.answer(text="❌ Товар не найден, попробуйте отправить ссылку вместо артикула или наоборот")
    except WildberriesAPIUncorrectedQuery:
        await message.answer(text="❌ Это не похоже на артикул или ссылку")
    except DatabaseExecuteQueryError:
        await message.answer(text="⚠️ Ошибка с базой данных, повторите попытку или обратитесь к разработчику")
