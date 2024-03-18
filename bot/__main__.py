import asyncio

from bot.services import dp
from loguru import logger
from aiogram import executor
import handlers
from aiogram import types
from bot import filters


async def set_default_settings_bot(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Главное меню"),
            types.BotCommand("help", "Помощь"),
            types.BotCommand("truncate", "Очистить позиции"),
        ]
    )


async def on_startup(dp):
    logger.add(
        "logs/avia_bot_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="7 days",
        compression="zip",
        level="DEBUG",
    )
    await set_default_settings_bot(dp=dp)
    logger.warning("The bot is started!")


async def on_shutdown(dp):
    logger.warning("The bot is stop!")


async def start_scheduler():
    logger.warning("Планировщик запущен!")


def main():
    loop = asyncio.get_event_loop()
    loop.create_task(start_scheduler())
    filters.setup(dp=dp)
    executor.start_polling(dp, loop=loop, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)


if __name__ == "__main__":
    main()
