from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def profile_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    kb_data = [
        ['Мой баланс', 'my_balance'],
        ['Мои заказы', 'my_orders'],
        ['Мои адреса', 'my_addresses'],
        ['Мои способы оплаты', 'my_payment_methods'],
        ['⬅️ Вернуться в меню', 'main_menu'],
    ]

    for button_data in kb_data:
        builder.button(text=button_data[0], callback_data=button_data[1])
    builder.adjust(1)
    return builder.as_markup()
