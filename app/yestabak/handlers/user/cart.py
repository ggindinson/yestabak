from datetime import datetime
from aiogram import exceptions
from aiogram import F, Bot
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from yestabak.handlers.user.profile import my_addresses
from yestabak.keyboards.addresses_builder import addresses_kb
from yestabak.handlers.user.start import start_handler
from yestabak.routes import userRouter
from yestabak.keyboards import cart_kb
from yestabak.api_wrapper import ApiWrapper
from yestabak.states import CartState
from yestabak.configs.config import CHAT_ID, CART_IMAGE


@userRouter.callback_query(F.data == "my_cart", StateFilter("*"))
async def my_cart(call: CallbackQuery, state: FSMContext, api: ApiWrapper):
    await state.set_state(CartState.cart)
    local_cart = (await state.get_data()).get("cart", [])
    print("Local Cart:", local_cart)

    # Replace user's local cart with user's api cart
    # await state.update_data(cart=user_cart)

    # Replace user's local cart with user's local cart
    # await state.update_data(cart=local_cart)

    # Replace user's api cart with user's local cart
    await api.post_cart(call.from_user.id, local_cart)

    # Get user's api cart
    user_cart = await api.get_user_cart(user_id=call.from_user.id)

    await call.message.edit_media(
        media=InputMediaPhoto(
            media=CART_IMAGE,
            caption="<b>1) Выберите товар\n2) Внесите изменения</b>"
            if len(user_cart)
            else "Ваша корзина пуста ❌",
        ),
        reply_markup=cart_kb(user_cart),
    )


@userRouter.callback_query(
    F.data.contains("delete_cartitem"), StateFilter(CartState.cart)
)
async def delete_cart_item(call: CallbackQuery, state: FSMContext):
    item_id = int(call.data.split("_")[-1])
    current_cart = (await state.get_data())["cart"]
    updated_cart = list(filter(lambda item: item["item_id"] != item_id, current_cart))
    await state.update_data(cart=updated_cart)
    await call.message.edit_reply_markup(reply_markup=cart_kb(updated_cart))


@userRouter.callback_query(F.data == "procedure_order")
async def procedure_order(call: CallbackQuery, api: ApiWrapper, state: FSMContext):
    user = await api.get_user_if_exists(call.from_user.id)
    addresses = user.addresses

    if not user.cart_items or len(user.cart_items) == 0:
        await call.answer(
            text="Корзина пуст! \nСначала добавьте товар в корзину!",
            show_alert=True,
        )
        await my_cart(call, state, api)
        return
    
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
    user = await api.get_user_if_exists(call.from_user.id)
    address = list(filter(lambda address: address.id == address_id, user.addresses))[0]

    # if not user.addresses or len(user.addresses) == 0:
    #     await call.answer(
    #         text="Вы не добавляли адрес для доставки. \nПерейдите в профиль и добавьте адрес!",
    #         show_alert=True,
    #     )
    #     return

    formatted_text = (
        f"✅ Поступил заказ! \n"
        + f"Заказчик (реальное фио): <a href=\"tg://user?id={call.from_user.id}\">{user.user.first_name} {user.user.last_name if user.user.last_name else ''}</a> \n"
        + f"Телеграм: <a href=\"tg://user?id={call.from_user.id}\">{call.from_user.first_name} {call.from_user.last_name if call.from_user.last_name else ''}</a> \n"
        + f"Номер телефона: {user.user.phone_number} \n"
        + f"Адрес: <code>{address.data['address']}</code> \n"
        + f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \n"
        + f"Товары: "
    )
    for item in user.cart_items:
        formatted_text += f"\n ~ [{item.quantity} шт.] {item.name}"

    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"Перейти к {call.from_user.full_name}",
        url=f"tg://user?id={call.from_user.id}",
    )

    try:
        await bot.send_message(CHAT_ID, formatted_text, reply_markup=builder.as_markup())
        await api.post_cart(call.from_user.id, [])
        await call.answer(
            "Заказ оформлен ✅ \nС вами в скором времени свяжется наш сотрудник! 😎",
            show_alert=True,
        )
        await state.clear()
        await start_handler(call, state, api)
    except exceptions.TelegramBadRequest as err:
        if "BUTTON_USER_PRIVACY_RESTRICTED" in err.message:
            formatted_text = (
                f"✅ Поступил заказ! \n"
                + f"Заказчик (реальное фио): <a href=\"tg://user?id={call.from_user.id}\">{user.user.first_name} {user.user.last_name if user.user.last_name else ''}</a> \n\n"
                + f"Телеграм: <a href=\"tg://user?id={call.from_user.id}\">{call.from_user.first_name} {call.from_user.last_name if call.from_user.last_name else ''}</a> \n"
                + f"<b><i>⚠️ Телеграм пользователя приватный, скорее всего через телеграм вы с ним никак не свяжетесь!</i></b> \n\n"
                + f"Номер телефона: {user.user.phone_number} \n"
                + f"Адрес: <code>{address.data['address']}</code> \n"
                + f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \n"
                + f"Товары: "
            )
            for item in user.cart_items:
                formatted_text += f"\n ~ [{item.quantity} шт.] {item.name}"
        
            await bot.send_message(CHAT_ID, formatted_text)
        
            await api.post_cart(call.from_user.id, [])
            await call.answer(
                "Заказ оформлен ✅ \n⚠️ НО! Пункт «Пересылка сообщений» в настройках вашего аккаунта НЕ позволяет нам связаться с вами через телеграм. \n😎 Всё же, мы сделаем всё возможное, чтобы связаться с вами!",
                show_alert=True,
            )
            await state.clear()
            await start_handler(call, state, api)

