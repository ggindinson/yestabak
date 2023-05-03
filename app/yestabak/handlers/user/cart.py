from aiogram import F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from yestabak.routes import userRouter
from yestabak.keyboards import items_kb
from yestabak.api_wrapper import ApiWrapper


@userRouter.callback_query(F.data == "my_cart", StateFilter("*"))
async def my_cart(call: CallbackQuery, state: FSMContext, api: ApiWrapper):
    await state.clear()

    user_cart = await api.get_user_cart(user_id=call.from_user.id)

    await call.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile("yestabak/assets/cart.jpg"),
            caption="<b>1) Выберите товар\n2) Внесите изменения</b>",
        ),
        reply_markup=items_kb(user_cart, user_cart),
    )
