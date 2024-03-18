from bot.utils.models import Product


def wb_create_product_message(product: Product) -> str:
    # TODO сделать обработку списка list[Product]
    return (
        f"✅ Позиция добавлена:\n\n"
        f"<b>{product.brand} {product.name} {product.colors}</b>\n"
        f"<b>Цена:</b> {product.total_price} руб. (~{product.wallet_price})\n"
        f"<b>В наличии:</b> {product.count} шт.\n"
        f"<b>Артикул:</b> <code>{product.article}</code>\n\n"
        # f"🟣 <i>Wildberries</i>\n"
    )
    # return message
