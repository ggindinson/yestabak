from typing import List
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

from yestabak.api_wrapper.api_classes import Address


def format_address(address: str):
    # return address[:-10] + "..." if len(address) > 10 else address
    return address[:-10] + "..." if len(address) > 20 else address


def addresses_kb(addresses: List[Address]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for address in addresses:
        builder.button(
            text=format_address(address.data["name"]),
            callback_data=f"address_additional_{address.id}",
        )
    builder.button(text="Добавить новый адрес", callback_data="add_address")
    builder.button(text="◀️ В личный кабинет", callback_data="my_profile")
    builder.adjust(1)
    return builder.as_markup()


def edit_address_kb(address_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Удалить адрес", callback_data=f"delete_address_{address_id}")
    builder.button(text="◀️ К адресам", callback_data="my_addresses")
    builder.adjust(1)
    return builder.as_markup()


def cancel_address_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Отменить создание ⚠", callback_data="my_addresses")
    return builder.as_markup()
