from aiogram import F
from aiogram.types import CallbackQuery, InputMediaPhoto, URLInputFile, FSInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from yestabak.routes import userRouter
from yestabak.utils import cart_dispatch
from yestabak.keyboards import items_kb


@userRouter.callback_query(F.data.contains("item"), StateFilter("*"))
async def handle_item_click(call: CallbackQuery, state: FSMContext):
    _, item_id, event_type = call.data.split("_")
    state_data = await state.get_data()
    current_cart = state_data["cart"]
    items = state_data["items"]
    current_item_info_id = state_data.get("current_item_info_id")

    for item in items:
        if item["id"] == int(item_id):
            item_clicked = item
            break

    cart = cart_dispatch(
        int(item_id),
        event_type,
        current_cart,
    )
    await state.update_data(cart=cart)

    if event_type == "increase" and int(item_id) != current_item_info_id:
        await call.message.edit_caption(
            caption=f"""Выбранный товар: {item_clicked["name"]}
Описание: {item_clicked["description"]}
Цена: {item_clicked["price"]}"""
        )

        if "https" in item_clicked["photo"]:
            await call.message.edit_media(
                InputMediaPhoto(media=URLInputFile(url=item_clicked["photo"]))
            )
        else:
            await call.message.edit_media(InputMediaPhoto(media=item_clicked["photo"]))

        await state.update_data(current_item_info_id=int(item_id))

    if (event_type == "decrease" or event_type == "delete") and not len(cart):
        await call.message.edit_media(
            InputMediaPhoto(
                media=FSInputFile("yestabak/assets/items.jpg"),
                caption="<b>1. Выберите товар\n2. Добавьте в корзину</b>",
            ),
        )

    await call.message.edit_reply_markup(reply_markup=items_kb(items, cart))
