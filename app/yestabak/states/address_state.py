from aiogram.fsm.state import State, StatesGroup


class AddressState(StatesGroup):
    menu = State()
    get_name = State()
    get_address = State()
