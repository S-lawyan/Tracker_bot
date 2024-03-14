from services import dp
from loguru import logger
from aiogram import executor
import handlers
from aiogram import types


async def set_default_settings_bot(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Главное меню"),
            types.BotCommand("cmd", "Заглушка"),
            types.BotCommand("help", "Помощь"),
        ]
    )


async def on_startup(dp):
    logger.warning("Starting bot...")
    logger.add(
        "bot/logs/avia_bot_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="7 days",
        compression="zip",
        level="DEBUG",
    )
    await set_default_settings_bot(dp=dp)
    logger.warning("The bot is started!")


async def on_shutdown(dp):
    logger.warning("The bot is stop!")


def main():
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)


if __name__ == "__main__":
    main()
