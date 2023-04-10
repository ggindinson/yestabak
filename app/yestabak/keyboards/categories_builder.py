from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def categories_kb(categories: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(
            text=category["name"], callback_data=f"category_{category['id']}"
        )
    builder.adjust(2)
    builder.row(
        InlineKeyboardButton(text="⬅️ Вернуться в меню", callback_data="main_menu")
    )
    return builder.as_markup()
