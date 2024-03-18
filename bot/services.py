from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.config import config
from database.sqlite import SQLiteBase
from api.wb_adapter import WildberriesAPI
from api.http_session import HttpSessionMaker
# from api.ozon_adapter import OzonAPI


storage: SQLiteBase = SQLiteBase(config)
wb: WildberriesAPI = WildberriesAPI(http_session_maker=HttpSessionMaker())
# ozon: OzonAPI = OzonAPI(config)
bot: Bot = Bot(token=config.bot.bot_token.get_secret_value(), parse_mode=types.ParseMode.HTML)
dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())
