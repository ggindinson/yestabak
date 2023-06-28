from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    get_category = State()
