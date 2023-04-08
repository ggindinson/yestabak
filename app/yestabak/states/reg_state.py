from aiogram.fsm.state import State, StatesGroup


class RegState(StatesGroup):
    get_first_name = State()
    get_last_name = State()
    get_phone = State()
