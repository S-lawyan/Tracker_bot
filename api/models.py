from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Product:
    name: str  # Наименование товара
    price: int  # Цена товара
    count: int  # Количество товара
    review_rating: float  # Рейтинг продавца по отзывам
    feedbacks: int  # Количество отзывов
    # supplier_rating: int  # Рейтинг продавца

