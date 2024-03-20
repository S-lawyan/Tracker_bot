from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Product:
    article: int
    name: str  # Наименование товара
    brand: str
    colors: str
    total_price: int  # Цена товара
    wallet_price: int  # Цена товара со скидкой по вб-кошельку
    count: int  # Количество товара
    supplier: str  # Название продавца
    supplier_id: int  # Идентификатор продавца
    # review_rating: float  # Рейтинг товара по отзывам
    # feedbacks: int  # Количество отзывов
    # supplier_rating: int  # Рейтинг продавца

