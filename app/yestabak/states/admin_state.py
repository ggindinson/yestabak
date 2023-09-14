from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    get_category = State()
    get_update_data = State()
    get_item_name = State()
    get_item_photo = State()
    get_item_description = State()
    get_item_price = State()
    import_from_excel = State()
