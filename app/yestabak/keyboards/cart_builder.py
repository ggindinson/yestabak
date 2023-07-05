from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def cart_kb(items) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in items:
        name = item["name"]
        builder.button(
            text=f"{name} ({item['quantity']} шт.)",
            callback_data=f"category_{item['category_id']}",
        )
        builder.button(
            text=f"🗑️ Убрать {name} из корзины",
            callback_data=f"delete_cartitem_{item['id']}",
        )
    builder.button(text="🎯 Оформить заказ", callback_data="payment_start") if len(
        items
    ) else builder.button(text="➡️ К категориям", callback_data="all_categories")
    builder.button(text="❌ Закрыть корзину", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()
