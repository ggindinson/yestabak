from aiogram.filters.callback_data import CallbackData
from datetime import datetime


class Item(CallbackData, prefix="item"):
    id: int | str
    category_id: int | str
    # price: str
    # name: str
    # description: str
    # photo: str
    # created_at: str
    # last_updated_at: str
