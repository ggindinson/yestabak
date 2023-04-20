from typing import List, Tuple
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dataclasses import dataclass


@dataclass
class SelectedItem:
    item_id: int
    quantity: int


def check_id_in_cart(
    id_to_check: int, items: List[SelectedItem]
) -> Tuple[bool, SelectedItem]:
    for item in items:
        if item["item_id"] == id_to_check and item["quantity"]:
            return True, item
    return False, None


def items_kb(items, selected_items: List[SelectedItem]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    is_cart_filled = False
    for item in items:
        item_id = item["id"]
        check_result, item_from_cart = check_id_in_cart(item_id, selected_items)

        if not check_result:
            builder.row(
                InlineKeyboardButton(
                    text=item["name"], callback_data=f"item_{item_id}_increase"
                )
            )
            continue
        builder.row(
            InlineKeyboardButton(
                text=f'✅ {item["name"]}',
                callback_data=f"item_{item_id}_delete",
            )
        )
        builder.row(
            InlineKeyboardButton(
                text="-1",
                callback_data=f"item_{item_id}_decrease",
            ),
            InlineKeyboardButton(
                text=item_from_cart["quantity"], callback_data=f"current_quantity"
            ),
            InlineKeyboardButton(
                text="+1",
                callback_data=f"item_{item_id}_increase",
            ),
        )
        is_cart_filled = True

    if is_cart_filled:
        builder.row(
            InlineKeyboardButton(text="🔺 Перейти в корзину", callback_data="my_cart")
        )

    builder.row(
        InlineKeyboardButton(text="👈 К категориям", callback_data="all_categories"),
        InlineKeyboardButton(text="👈 В меню", callback_data="main_menu"),
    )

    return builder.as_markup()
