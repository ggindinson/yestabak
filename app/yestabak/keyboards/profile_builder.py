from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def profile_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    kb_data = [
        ["Мои адреса", "my_addresses"],
        ["Мои покупки", "my_orders"],
        ["⬅️ Вернуться в меню", "main_menu"],
    ]

    for button_data in kb_data:
        builder.button(text=button_data[0], callback_data=button_data[1])
    builder.adjust(1)
    return builder.as_markup()
