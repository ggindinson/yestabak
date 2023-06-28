from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def start_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔥 К выбору категории", callback_data="all_categories")
    builder.button(text="👤 Личный кабинет", callback_data="my_profile")
    builder.button(text="🛒 Корзина", callback_data="my_cart")
    builder.adjust(1)
    return builder.as_markup()
