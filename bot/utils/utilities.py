from bot.utils.models import Product


def wb_create_product_message(product: Product) -> str:
    # TODO сделать обработку списка list[Product]
    return (
        f"✅ Позиция добавлена:\n\n"
        f"<b>{product.brand} {product.name} {product.colors}</b>\n"
        f"<b>Цена:</b> {product.total_price} руб. (~{product.wallet_price})\n"
        f"<b>В наличии:</b> {product.count} шт.\n"
        f"<b>Продавец</b> <u><a href='https://www.wildberries.ru/seller/{product.supplier_id}'>{product.supplier}</a></u>"
        f"<b>Артикул:</b> <code>{product.article}</code>\n\n"
        f"🟣 <i>WB</i>"
    )
    # return message


def wb_alert_user(old_product: Product, new_product: Product) -> str:
    return (
        f"⚡⚡⚡ <b>Цена снижена</b>\n\n"
        f"{new_product.brand} {new_product.name} {new_product.colors}\n"
        f"<b>Старая цена:</b> {old_product.total_price} руб. (~{old_product.wallet_price})\n"
        f"<b>Новая цена:</b> {new_product.total_price} руб. (~{new_product.wallet_price})\n"
        f"<b>Продавец:</b> <u><a href='https://www.wildberries.ru/seller/{new_product.supplier_id}'>{new_product.supplier}</a></u>\n"
        f"<b>Артикул:</b> <code>{new_product.article}</code>"
        f"\n\n"
        f"🟣 <i>WB</i>"
    )
