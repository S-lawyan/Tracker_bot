import os
from dotenv import load_dotenv

from pydantic import BaseModel, SecretStr


class BotConfig(BaseModel):
    bot_token: SecretStr
    per_page: int


class SQLiteConfig(BaseModel):
    db_filename: str


class Settings(BaseModel):
    db: SQLiteConfig
    bot: BotConfig


def load_config(config_path: str) -> Settings:
    load_dotenv(dotenv_path=config_path)
    bot_configs: BotConfig = BotConfig(
        bot_token=SecretStr(os.getenv("BOT_TOKEN", None)),
        per_page=os.getenv("PER_PAGE", None)
    )
    db_configs: SQLiteConfig = SQLiteConfig(
        db_filename=os.getenv("DB_FILENAME", None)
    )
    return Settings(db=db_configs, bot=bot_configs)


# Получаю директорию бота
BOT_DIR = os.path.dirname(os.path.abspath(__file__))
# Получаю директорию проекта
PROJECT_DIR = os.path.dirname(BOT_DIR)
# Подгружаю конфиги и запускаю бота
config: Settings = load_config(config_path=os.path.join(PROJECT_DIR, ".env"))

__all__ = ["config", "Settings"]
