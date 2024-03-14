from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.config import config
from database.sqlite import SQLiteBase

storage = SQLiteBase(config)
bot = Bot(token=config.bot.bot_token.get_secret_value(), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
