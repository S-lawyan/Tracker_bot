from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot.keyboards.client_kb import *
from aiogram.dispatcher.filters import Text
from bot.services import dp, storage


# ================= БЛОК ОСНОВНЫХ КОМАНД БОТА ==============================
@dp.message_handler(commands=["start"], state=None)
async def command_start(message: types.Message) -> None:
    if message.chat.id == -4126813172:
        return
    if await es.check_in_consumers_index(field="tg_id", value=int(message.from_user.id)):
        await message.answer(text=glossary.get_phrase("consumer_main_menu"), reply_markup=consumer_panel_main)
    else:
        await message.answer(
            text=glossary.get_phrase(
                "start_greeting",
                username=message.from_user.first_name
            ),
            reply_markup=kb_registration,
        )


@dp.message_handler(IsDirect(), commands=["help"], state='*')
@dp.message_handler(IsDirect(), Text(startswith="помощь", ignore_case=True), state='*')
async def command_help_message(message: types.Message) -> None:
    await message.answer(text=glossary.get_phrase("help"))