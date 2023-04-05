from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from yestabak.api_wrapper import ApiWrapper
from yestabak.routes.user.router import userRouter
from yestabak.keyboards import categories_kb


@userRouter.callback_query(F.data == "all_categories", StateFilter("*"))
async def start_handler(call: CallbackQuery, state: FSMContext, api: ApiWrapper):
    await state.clear()

    categories = await api.get_categories()
    await call.message.delete()

    await call.message.answer_photo(
        FSInputFile("yestabak/assets/categories.jpg"),
        caption="<b>Выберите категорию</b>",
        reply_markup=categories_kb(categories),
    )
