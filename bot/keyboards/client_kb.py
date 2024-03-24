from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton


btn_confirm = InlineKeyboardButton(text="Да, удалить ✅", callback_data='confirm')
btn_cancel = InlineKeyboardButton(text="Отмена 🚫", callback_data='cancel')

kb_confirm_deletion = InlineKeyboardMarkup()
kb_confirm_deletion.add(btn_confirm, btn_cancel)

kb_cancel = InlineKeyboardMarkup()
kb_cancel.add(btn_cancel)

btn_product_list = KeyboardButton(text="Список позиций 📋", command='list')
btn_help = KeyboardButton(text="Помощь 🆘", command='help')
btn_delete_one_product = KeyboardButton(text="Удалить 1 позицию", command="drop_one")
btn_drop_all_products = KeyboardButton(text="Удалить все 🗑", command="drop_all")
admin_panel_main = ReplyKeyboardMarkup(
    resize_keyboard=True
).add(btn_product_list, btn_help).add(btn_delete_one_product, btn_drop_all_products)


async def pagination(total_pages: int, page: int = 0):
    return InlineKeyboardMarkup().row(
        InlineKeyboardButton(text="⬅", callback_data=f"previous:{page}"),
        InlineKeyboardButton(text=f"{page+1}/{total_pages}", callback_data="None"),
        InlineKeyboardButton(text="➡", callback_data=f"next:{page}"),
    )
