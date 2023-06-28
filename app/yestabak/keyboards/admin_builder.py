from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def admin_items_menu(items):
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.button(item["name"], callback_data=f"admin_item_{item['id']}")
    builder.button("Удалить категорию ⚠", callback_data=f"admin_delete_category_{}")
    builder.button("Назад к категориям 🔙", callback_data=f"admin_categories")
    builder.adjust(1)
    return builder.as_markup()


def admin_single_item_menu(item_id: int):
    builder = InlineKeyboardBuilder()
    builder.add("Изменить имя товара", callback_data=f"change_item_name_{item_id}")
    builder.add(
        "Изменить описание товара", callback_data=f"change_item_description_{item_id}"
    )
    builder.add("Изменить цену товара", callback_data=f"change_item_price_{item_id}")
    builder.add("Изменить фото товара", callback_data=f"change_item_photo_{item_id}")
    builder.adjust(1)
    return builder.as_markup()
