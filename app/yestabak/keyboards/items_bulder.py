from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def items_kb(items: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.button(text=item["name"], callback_data=f"item_{item['id']}")
    builder.adjust(2)
    builder.button(text="⬅️ Выбрать другую категорию", callback_data="all_categories")
    builder.button(text="⬅️ Вернуться в меню", callback_data="main_menu")
    builder.adjust(1)

    return builder.as_markup()
