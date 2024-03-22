import math

from aiogram import types
from aiogram.dispatcher.filters import Text
from bot.config import config
from bot.keyboards.client_kb import *
from bot.services import dp
from bot.services import wb_api
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
from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.dispatcher import FSMContext


class UserState(StatesGroup):
    confirm_state = State()
    await_article = State()


# ================= БЛОК ОСНОВНЫХ КОМАНД БОТА ==============================
@dp.message_handler(IsAdmin(), commands=["start"], state=None)
@dp.message_handler(IsAdmin(), Text(startswith="меню", ignore_case=True), state=None)
@dp.message_handler(IsAdmin(), Text(startswith="главное меню", ignore_case=True), state=None)
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


@dp.message_handler(IsAdmin(), commands=["help"], state=None)
@dp.message_handler(IsAdmin(), Text(startswith="помощь", ignore_case=True), state=None)
async def command_help_message(message: types.Message) -> None:
    await message.answer(text="help")


@dp.message_handler(IsAdmin(), commands=["show_products_list"], state=None)
@dp.message_handler(IsAdmin(), Text(startswith="список", ignore_case=True), state=None)
@dp.message_handler(IsAdmin(), Text(startswith="список позиций", ignore_case=True), state=None)
async def get_product_list(message: types.Message):
    products_poll: list[Product] = await storage.get_products_by_user(user_id=int(message.from_user.id))
    if len(products_poll) == 0:
        await message.answer(text="У вас нет товаров в отслеживании")
    else:
        total_pages: int = math.ceil(len(products_poll) / config.bot.per_page)
        message_text = await send_products_list(products_list=products_poll)
        await message.answer(text=message_text, reply_markup=await pagination(total_pages=total_pages))


@dp.message_handler(IsAdmin(), commands=["drop_all"], state=None)
@dp.message_handler(IsAdmin(), Text(startswith="удалить все", ignore_case=True), state=None)
async def delete_all_products(message: types.Message, state: FSMContext):
    sent_message = await message.answer(text="⚠️ Удалить <b>все</b> записи из БД?", reply_markup=kb_confirm_deletion)
    async with state.proxy() as data:
        data['sent_message'] = sent_message
    await UserState.confirm_state.set()


@dp.message_handler(IsAdmin(), commands=["drop_one"], state=None)
@dp.message_handler(IsAdmin(), Text(startswith="удалить 1 позицию", ignore_case=True), state=None)
async def await_article(message: types.Message, state: FSMContext):
    sent_message = await message.answer(text="Отправьте артикул товара для удаления", reply_markup=kb_cancel)
    async with state.proxy() as data:
        data['sent_message'] = sent_message
    await UserState.await_article.set()


@dp.message_handler(IsAdmin(), content_types=['text'], state=UserState.await_article)
async def delete_one_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        sent_message: types.Message = data['sent_message']
    await sent_message.edit_reply_markup(reply_markup=None)
    try:
        article: int = int(message.text)
        if not await storage.check_product(user_id=int(message.from_user.id), article=article):
            await storage.delete_one_product(user_id=int(message.from_user.id), article=article)
            await message.answer(f"✅ Товар <code>{article}</code> успешно удален")
        else:
            await message.reply(f"Товара с таким артикулом нет в списке отслеживаемых")
        await state.finish()

    except (ValueError,):
        await message.answer("⚠️ В артикуле допущена ошибка, повторите попытку")


@dp.callback_query_handler(IsAdmin(), text=["confirm"], state=UserState.confirm_state)
async def confirming_delete_all(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        sent_message: types.Message = data['sent_message']
    await sent_message.edit_reply_markup(reply_markup=None)
    try:
        await storage.drop_all_products(user_id=int(call.from_user.id))
        await call.message.answer(text="✅ Все ваши товары удалены из списка отслеживаемых")
    except DatabaseExecuteQueryError:
        await call.message.answer(text="⚠️ Ошибка с базой данных, повторите попытку или обратитесь к разработчику")
    finally:
        await state.finish()


@dp.callback_query_handler(IsAdmin(), text=["cancel"], state=UserState.confirm_state)
@dp.callback_query_handler(IsAdmin(), text=["cancel"], state=UserState.await_article)
async def cancel(call: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            sent_message: types.Message = data['sent_message']
        await sent_message.edit_reply_markup(reply_markup=None)
    except (Exception,):
        pass
    finally:
        current_state = await state.get_state()
        if current_state is not None:
            await state.finish()


@dp.message_handler(IsAdmin(), content_types=['text'], state=None)
async def get_query(message: types.Message):
    query: str = message.text
    try:
        product: Product = await wb_api.get_product(query=query)
        if not await storage.check_product(user_id=int(message.from_user.id), article=product.article):
            await storage.insert_product(product=product, user_id=int(message.from_user.id))
            await message.answer(text=utl.wb_create_product_message(product=product), reply_markup=None)
        else:
            await message.reply("Этот товар уже отслеживается")
    except (
            WildberriesAPIGetProductTimeout,
            WildberriesAPIClientConnectionError,
    ):
        await message.answer(text="❌ Произошла ошибка, повторите попытку")
    except WildberriesAPIProductNotFound:
        await message.answer(text="❌ Товар не найден, попробуйте отправить ссылку вместо артикула или наоборот")
    except WildberriesAPIUncorrectedQuery:
        await message.answer(text="❌ Это не похоже на артикул или ссылку на товар Wildberries")
    except DatabaseExecuteQueryError:
        await message.answer(text="⚠️ Ошибка с базой данных, повторите попытку или обратитесь к разработчику")


async def send_products_list(products_list: list[Product], page: int = 0) -> str:
    per_page = config.bot.per_page
    start_index: int = page * per_page
    end_index: int = start_index + per_page
    products_on_page: list[Product] = products_list[start_index:end_index]

    return await utl.generate_page_product(products=products_on_page)


@dp.callback_query_handler(lambda query: query.data.startswith("previous:"), state=None)
async def previous_page(call: types.CallbackQuery):
    products_poll: list[Product] = await storage.get_products_by_user(user_id=int(call.from_user.id))
    total_pages: int = math.ceil(len(products_poll) / config.bot.per_page)
    page = int(call.data.split(":")[1]) - 1 if int(call.data.split(":")[1]) > 0 else 0
    message_text = await send_products_list(products_list=products_poll, page=page)
    try:
        await call.message.edit_text(
            text=message_text,
            reply_markup=await pagination(
                total_pages=total_pages,
                page=page
            )
        )
    except (IndexError, KeyError):
        pass


@dp.callback_query_handler(lambda query: query.data.startswith("next:"), state=None)
async def next_page(call: types.CallbackQuery):
    products_poll: list[Product] = await storage.get_products_by_user(user_id=int(call.from_user.id))
    total_pages: int = math.ceil(len(products_poll) / config.bot.per_page)
    page = int(call.data.split(":")[1]) + 1 if int(call.data.split(":")[1]) < (total_pages-1) else (total_pages-1)
    message_text = await send_products_list(products_list=products_poll, page=page)
    try:
        await call.message.edit_text(
            text=message_text,
            reply_markup=await pagination(
                total_pages=total_pages,
                page=page
            )
        )
    except (IndexError, KeyError):
        pass
