from aiogram.fsm.state import State, StatesGroup


class CartState(StatesGroup):
    cart = State()
