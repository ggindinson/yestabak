from aiogram import F
from aiogram.types import CallbackQuery, InputMediaPhoto, URLInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from yestabak.routes import userRouter
from yestabak.utils import cart_dispatch
from yestabak.keyboards import items_kb


@userRouter.callback_query(F.data.contains("item"), StateFilter("*"))
async def handle_item_click(call: CallbackQuery, state: FSMContext):
    _, item_id, event_type = call.data.split("_")
    items = (await state.get_data())["items"]
    for item in items:
        if item["id"] == int(item_id):
            item_clicked = item
            break

    current_cart = (await state.get_data())["cart"]

    cart = cart_dispatch(
        int(item_id),
        event_type,
        current_cart,
    )
    await state.update_data(cart=cart)

    if event_type == "increase":
        try:
            await call.message.edit_media(InputMediaPhoto(media=item_clicked["photo"]))
        except TelegramBadRequest:
            await call.message.edit_media(
                InputMediaPhoto(media=URLInputFile(url=item_clicked["photo"]))
            )
        await call.message.edit_caption(
            caption=f"""Выбранный товар: {item_clicked["name"]}
Описание: {item_clicked["description"]}
Цена: {item_clicked["price"]}"""
        )

    await call.message.edit_reply_markup(reply_markup=items_kb(items, cart))
