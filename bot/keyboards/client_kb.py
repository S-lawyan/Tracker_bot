from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton


kb_confirm_deletion = InlineKeyboardMarkup()
kb_confirm_deletion.add(
    InlineKeyboardButton(text="Да, удалить", callback_data='confirm'),
    InlineKeyboardButton(text="Отмена", callback_data='cancel'),
)


btn_product_list = KeyboardButton(text="Список позиций 📋", command='show_product_list')
btn_help = KeyboardButton(text="Помощь 🆘", command='help')
btn_delete_one_product = KeyboardButton(text="Удалить 1 позицию", command="del_one")
btn_drop_all_products = KeyboardButton(text="Удалить все 🗑", command="drop_all")
admin_panel_main = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_product_list, btn_help).add(btn_delete_one_product, btn_drop_all_products)


# btn_cancel = KeyboardButton(text="Отмена", command='cancel')
# kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_cancel)


async def pagination(total_pages: int, page: int = 0):
    return InlineKeyboardMarkup().row(
        InlineKeyboardButton(text="⬅", callback_data=f"previous:{page}"),
        InlineKeyboardButton(text=f"{page+1}/{total_pages}", callback_data="None"),
        InlineKeyboardButton(text="➡", callback_data=f"next:{page}"),
    )
