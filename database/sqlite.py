import json
import sqlite3 as sq
from typing import Any

from bot.config import Settings
from loguru import logger
from bot.utils.models import Product
from bot.utils.exceptions import (
    DatabaseExecuteQueryError,

)


class SQLiteBase:
    def __init__(self, config: Settings):
        self.connect = sq.connect(
            database="../database/" + config.db.db_filename
        )
        if self.connect:
            logger.warning("The connection to the database has been completed successfully!")
            self._create_scheme()

    def _create_scheme(self) -> None:
        """Создание схемы БД"""
        with self.connect as connect:
            connect.execute("""
                CREATE TABLE IF NOT EXISTS "products" (
                    "id"	INTEGER,
                    "user_id"	INTEGER,
                    "article"	INTEGER,
                    "data"	TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT)
                )
            """)
            connect.execute("""
                CREATE TABLE IF NOT EXISTS "settings" (
                    "user_id"	INTEGER UNIQUE,
                    "difference "	INTEGER DEFAULT 10
                )
            """)
            connect.commit()

    async def _execute_query(self, query: str, params: tuple = None) -> Any:
        try:
            with self.connect as connect:
                result = connect.execute(query, params)
                connect.commit()
                return result
        except (Exception,) as exc:
            logger.error(f"Ошибка запроса к БД: {query}\nОшибка: {exc}")
            raise DatabaseExecuteQueryError()

    async def insert_user(self, user_id: int) -> None:
        query = f"""
            INSERT INTO settings (
                user_id
            ) 
            VALUES (?)
        """
        params = (user_id,)
        await self._execute_query(query=query, params=params)

    async def check_user(self, user_id: int) -> bool:
        with self.connect as connect:
            return bool(
                connect.execute(
                    "SELECT EXISTS(SELECT 1 FROM settings WHERE user_id = ?)", (user_id,)
                ).fetchone()[0]
            )

    async def insert_product(self, product: Product, user_id: int) -> None:
        query = f"""
            INSERT INTO products (
                user_id, 
                article, 
                data
            ) 
            VALUES (?, ?, ?)
        """
        params = (user_id, product.article, json.dumps(product.__dict__, ensure_ascii=False))
        await self._execute_query(query=query, params=params)

    async def get_all_products(self) -> dict:
        query = f"""
            SELECT * FROM products
        """
        params = ()
        response = await self._execute_query(query=query, params=params)
        rows: list = response.fetchall()
        return pars_response(rows)


def pars_response(rows: list[tuple]) -> dict:
    """
    Группировка либо по товарам
    :param rows: list[tuple]
    :return: rows_group_by_products {
            "product_id": {
                "users": [12345678, 87654321], # список пользователей, отслеживающих этот товар
                "data": {...} # метаданные товара
            }
        }
    """
    rows_group_by_products: dict = {}
    for row in rows:
        article: int = row[1]
        user_id: int = row[2]
        product_data: str = row[3]
        if article not in rows_group_by_products.keys():
            # Если товара еще нет в сгруппированном списке
            rows_group_by_products[article] = {
                "users": [user_id],
                "data": pars_product_from_json(json.loads(product_data))
            }
        else:
            # Если товар уже есть в сгруппированном списке -
            # дополняем список отслеживающих пользователей
            rows_group_by_products[article]["users"].appand(user_id)
    return rows_group_by_products


def pars_product_from_json(product: dict) -> Product:
    return Product(
        article=product.get("id", 0),
        name=product.get("name", ""),
        brand=product.get("brand", ""),
        colors=product.get("colors", ""),
        total_price=product.get("total_price", 0),
        wallet_price=product.get("wallet_price", 0),
        count=product.get("count", 0),
        review_rating=product.get("review_rating", 0),
        feedbacks=product.get("feedbacks", 0),
        # supplier_rating=product.get("supplierRating", 0)
    )

