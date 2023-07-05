from datetime import datetime
from aiogram import F, Bot
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from yestabak.handlers.user.profile import my_addresses
from yestabak.keyboards.addresses_builder import addresses_kb
from yestabak.handlers.user.start import start_handler
from yestabak.routes import userRouter
from yestabak.keyboards import cart_kb
from yestabak.api_wrapper import ApiWrapper
from yestabak.states import CartState
from yestabak.configs.config import CHAT_ID


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


@userRouter.callback_query(F.data == "procedure_order")
async def procedure_order(call: CallbackQuery, api: ApiWrapper, state: FSMContext):
    addresses = (await api.get_user_if_exists(call.from_user.id)).addresses
    if not len(addresses):
        await call.answer("Добавьте адреса в профиле для продолжения", show_alert=True)
        return await my_addresses(call, api, state)
    await call.message.delete()
    await call.message.answer(
        "Выберите адрес из добавленных вами ниже:",
        reply_markup=addresses_kb(addresses, is_order=True),
    )


@userRouter.callback_query(F.data.contains("finish_order"))
async def finish_order(
    call: CallbackQuery, state: FSMContext, api: ApiWrapper, bot: Bot
):
    address_id = int(call.data.split("_")[-1])
    await state.clear()
    user = await api.get_user_if_exists(call.from_user.id)
    address = list(filter(lambda address: address.id == address_id, user.addresses))[0]

    if not user.addresses or len(user.addresses) == 0:
        return

    formatted_text = (
        f"Поступил заказ! \n"
        + f"Заказчик: <a href=\"tg://openmessage?user_id={call.from_user.id}\">{call.from_user.first_name} {call.from_user.last_name if call.from_user.last_name else ''}</a> \n"
        + f"Номер телефона: {user.user.phone_number} \n"
        + f"Адрес: {address.data['address']} \n"
        + f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \n"
        + f"Товары: "
    )
    for item in user.cart_items:
        formatted_text += f"\n ~ [{item.quantity} шт.] {item.name}"

    await bot.send_message(CHAT_ID, formatted_text)

    await api.post_cart(call.from_user.id, [])
    await call.answer(
        "Заказ оформлен ✅ \nС вами в скором времени свяжется наш сотрудник! 😎",
        show_alert=True,
    )
    await start_handler(call, state, api)
