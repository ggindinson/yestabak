from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def categories_kb(categories: list, is_admin_menu=False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(
            text=category["name"],
            callback_data=f"{'admin_' if is_admin_menu else ''}category_{category['id']}",
        )
    builder.adjust(2)
    if is_admin_menu:
        builder.row(
            InlineKeyboardButton(
                text="✒ Создать категорию", callback_data="create_category"
            )
        )
    builder.row(
        InlineKeyboardButton(text="📩 Импортировать из Excel", callback_data="import_from_excel")
    )
    builder.row(
        InlineKeyboardButton(text="⬅️ Вернуться в меню", callback_data="main_menu")
    )
    return builder.as_markup()
