from typing import Union
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from yestabak.routes.user.router import userRouter
from yestabak.keyboards import start_menu_kb


@userRouter.message(F.text == "/start", StateFilter("*"))
@userRouter.callback_query(F.data == "main_menu", StateFilter("*"))
async def start_handler(message: Union[Message, CallbackQuery], state: FSMContext):
    await state.clear()

    if isinstance(message, CallbackQuery):
        message = message.message
        await message.delete()

    await message.answer_photo(
        photo=FSInputFile("yestabak/assets/menu.jpg"),
        caption="<b>Добро пожаловать!</b>",
        reply_markup=start_menu_kb(),
    )
