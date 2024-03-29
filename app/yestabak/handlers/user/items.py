from aiogram import F
from aiogram.types import CallbackQuery, InputMediaPhoto, URLInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from yestabak.configs.config import ITEMS_IMAGE
from yestabak.routes import userRouter
from yestabak.utils import cart_dispatch
from yestabak.keyboards import items_kb


@userRouter.callback_query(F.data.startswith("item"), StateFilter("*"))
async def handle_item_click(call: CallbackQuery, state: FSMContext):
    _, item_id, event_type = call.data.split("_")
    state_data = await state.get_data()
    current_cart = state_data["cart"]
    items = state_data["items"]
    current_item_info_id = state_data.get("current_item_info_id")
    print("items:", items)

    for item in items:
        item_clicked = None
        if item.get("id", item.get("item_id", None)) == int(item_id):
            item_clicked = item
            break

    for item in current_cart:
        item_in_cart = None
        if item.get("id", item.get("item_id", None)) == int(item_id):
            item_in_cart = item
            break

    if (
        event_type == "increase"
        and len(current_cart)
        and item_in_cart
        and item_in_cart["quantity"] > 19
    ):
        await call.answer(
            "Вы не можете добавить больше 20 единиц одного товара!", show_alert=True
        )
        return

    cart = cart_dispatch(
        int(item_id),
        event_type,
        current_cart,
    )
    await state.update_data(cart=cart)

    if event_type == "increase" and int(item_id) != current_item_info_id:
        caption = f"""<b>Выбранный товар:</b> <b><i>{item_clicked["name"]}</i></b>
<b>Описание:</b> <i>{item_clicked["description"]}</i>
<b>Цена:</b> <b><i>{item_clicked["price"]} {"рублей" if item_clicked["currency"] == "RUB" else ""}</i></b>"""

        await call.message.edit_media(
            InputMediaPhoto(
                media=URLInputFile(url=item_clicked["photo"])
                if "https" in item_clicked["photo"]
                else item_clicked["photo"],
                caption=caption,
            )
        )
        await state.update_data(current_item_info_id=int(item_id))

    if (event_type == "decrease" or event_type == "delete") and not len(cart):
        await call.message.edit_media(
            InputMediaPhoto(
                media=ITEMS_IMAGE,
                caption="<b>1. Выберите товар\n2. Добавьте в корзину</b>",
            ),
        )
        await state.update_data(current_item_info_id=0)

    await call.message.edit_reply_markup(reply_markup=items_kb(items, cart))
