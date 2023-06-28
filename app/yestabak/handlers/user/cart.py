from aiogram import F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from yestabak.routes import userRouter
from yestabak.keyboards import cart_kb
from yestabak.api_wrapper import ApiWrapper
from yestabak.states import CartState


@userRouter.callback_query(F.data == "my_cart", StateFilter("*"))
async def my_cart(call: CallbackQuery, state: FSMContext, api: ApiWrapper):
    await state.set_state(CartState.cart)

    user_cart = await api.get_user_cart(user_id=call.from_user.id)
    await state.update_data(cart=user_cart)
    await call.message.answer_photo(
        photo=FSInputFile("yestabak/assets/cart.jpg"),
        caption="<b>1) Выберите товар\n2) Внесите изменения</b>"
        if len(user_cart)
        else "Ваша корзина пуста ❌",
        reply_markup=cart_kb(user_cart),
    )


@userRouter.callback_query(
    F.data.contains("delete_cartitem"), StateFilter(CartState.cart)
)
async def delete_cart_item(call: CallbackQuery, state: FSMContext):
    item_id = int(call.data.split("_")[-1])
    current_cart = (await state.get_data())["cart"]
    updated_cart = list(filter(lambda item: item["id"] != item_id, current_cart))
    await state.update_data(cart=updated_cart)
    await call.message.edit_reply_markup(reply_markup=cart_kb(updated_cart))
