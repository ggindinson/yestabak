from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def contact_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Отправить номер телефона", request_contact=True)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
