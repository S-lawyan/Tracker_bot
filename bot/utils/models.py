from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Product:
    article: int
    name: str  # Наименование товара
    brand: str
    colors: str
    price: int  # Цена товара
    count: int  # Количество товара
    supplier: str  # Название продавца
    supplier_id: int  # Идентификатор продавца
    # review_rating: float  # Рейтинг товара по отзывам
    # feedbacks: int  # Количество отзывов
    # supplier_rating: int  # Рейтинг продавца

