from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from yestabak.api_wrapper import ApiWrapper
from yestabak.routes.user.router import userRouter
from yestabak.keyboards import categories_kb, items_kb


@userRouter.callback_query(F.data == "all_categories", StateFilter("*"))
async def categories_menu(call: CallbackQuery, state: FSMContext, api: ApiWrapper):
    await state.clear()

    categories = await api.get_categories()
    await call.message.delete()

    await call.message.answer_photo(
        FSInputFile("yestabak/assets/categories.jpg"),
        caption="<b>Выберите категорию</b>",
        reply_markup=categories_kb(categories),
    )


@userRouter.callback_query(F.data.contains("category"), StateFilter("*"))
async def single_category(call: CallbackQuery, state: FSMContext, api: ApiWrapper):
    await state.clear()
    await call.message.delete()
    category_id = int(call.data.split('_')[1])

    category_items = await api.get_category_items(category_id)

    await call.message.answer_photo(
        FSInputFile("yestabak/assets/items.jpg"),
        caption="<b>1. Выберите товар\n2. Добавьте в корзину</b>",
        reply_markup=items_kb(category_items),
    )
