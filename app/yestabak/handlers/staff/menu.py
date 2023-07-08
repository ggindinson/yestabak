from aiogram import F
from aiogram.types import Message, CallbackQuery, URLInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from yestabak.keyboards.items_builder import (
    admin_item_settings_kb,
    admin_back_kb,
    admin_items_kb,
    admin_cancel_kb,
)
from yestabak.routes import staffRouter
from yestabak.api_wrapper import ApiWrapper
from yestabak.states import AdminState
from yestabak.keyboards import categories_kb


@staffRouter.message(F.text == "/admin", StateFilter("*"))
@staffRouter.callback_query(F.data == "admin", StateFilter("*"))
async def admin_menu_handler(event: Message | CallbackQuery, api: ApiWrapper):
    categories = await api.get_categories()
    if isinstance(event, Message):
        await event.delete()
        await event.answer(
            "Добро пожаловать в админ-меню. Выберите категорию из списка ниже, чтобы начать с ней взаимодействовать, или создайте новую",
            reply_markup=categories_kb(categories, is_admin_menu=True),
        )
        return
    if not event.message.photo:
        await event.message.edit_text(
            "Добро пожаловать в админ-меню. Выберите категорию из списка ниже, чтобы начать с ней взаимодействовать, или создайте новую",
            reply_markup=categories_kb(categories, is_admin_menu=True),
        )
    else:
        await event.message.delete()
        await event.message.answer(
            "Добро пожаловать в админ-меню. Выберите категорию из списка ниже, чтобы начать с ней взаимодействовать, или создайте новую",
            reply_markup=categories_kb(categories, is_admin_menu=True),
        )


@staffRouter.callback_query(F.data.startswith("admin_category"))
async def admin_category_settings(call: CallbackQuery, api: ApiWrapper):
    category_id = int(call.data.split("_")[-1])
    items = await api.get_category_items(category_id)
    if not call.message.photo:
        await call.message.edit_text(
            "Здесь вы можете добавить/удалить/изменить товар(ы), а также удалить категорию",
            reply_markup=admin_items_kb(items, category_id),
        )
    else:
        await call.message.delete()
        await call.message.answer(
            "Здесь вы можете добавить/удалить/изменить товар(ы), а также удалить категорию",
            reply_markup=admin_items_kb(items, category_id),
        )


@staffRouter.callback_query(F.data.startswith("admin_item_settings"))
async def admin_item_settings(call: CallbackQuery, api: ApiWrapper):
    category_id = int(call.data.split("_")[-1])
    item_id = int(call.data.split("_")[-2])
    item = await api.get_item_by_id(item_id)
    await call.message.delete()
    await call.message.answer_photo(
        photo=URLInputFile(url=item["photo"])
        if "https" in item["photo"]
        else item["photo"],
        caption=f"Здесь вы можете отредактировать/удалить товар\n\n{item['name']}\n<b>Описание:</b> {item['description']}\n<b>Цена:</b> {item['price']}",
        reply_markup=admin_item_settings_kb(item, category_id),
    )


@staffRouter.callback_query(F.data.startswith("delete_category"))
async def delete_category(call: CallbackQuery, api: ApiWrapper):
    category_id = int(call.data.split("_")[-1])
    await api.delete_category(category_id=category_id)
    await call.message.edit_text(
        "✅ Категория успешно удалена", reply_markup=admin_back_kb()
    )


@staffRouter.callback_query(F.data == "create_category")
async def create_category(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.get_category)
    msg = await call.message.edit_text(
        "✒ Пришлите имя категории", reply_markup=admin_back_kb()
    )
    await state.update_data(msg=msg)


@staffRouter.message(StateFilter(AdminState.get_category))
async def send_category_data(message: Message, api: ApiWrapper, state: FSMContext):
    msg = (await state.get_data())["msg"]
    await api.create_category(message.text)
    await message.delete()
    await msg.edit_text("✅ Категория успешно добавлена", reply_markup=admin_back_kb())


@staffRouter.callback_query(F.data.startswith("delete_item"))
async def delete_item(call: CallbackQuery, api: ApiWrapper):
    item_id = call.data.split("_")[-1]
    await api.delete_item(item_id)
    await call.message.delete()
    await call.message.answer("✅ Товар успешно удален", reply_markup=admin_back_kb())


@staffRouter.callback_query(F.data.startswith("create_item"))
async def create_item(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split("_")[-1])
    await state.set_state(AdminState.get_item_name)
    msg = await call.message.edit_text(
        "Пришлите имя товара", reply_markup=admin_cancel_kb()
    )
    await state.update_data(msg=msg, category_id=category_id)


@staffRouter.message(StateFilter(AdminState.get_item_name))
async def proceed_item_name(message: Message, state: FSMContext):
    msg = (await state.get_data())["msg"]
    await state.set_state(AdminState.get_item_photo)

    await message.delete()
    await msg.edit_text(
        "Пришлите фотографию товара ссылкой, либо отправьте изображение",
        reply_markup=admin_cancel_kb(),
    )
    await state.update_data(msg=msg, name=message.text)


@staffRouter.message(StateFilter(AdminState.get_item_photo))
async def proceed_item_photo(message: Message, state: FSMContext):
    msg = (await state.get_data())["msg"]
    await state.set_state(AdminState.get_item_description)

    await message.delete()
    await msg.edit_text(
        "Пришлите описание товара",
        reply_markup=admin_cancel_kb(),
    )
    await state.update_data(
        msg=msg, photo=message.text if message.text else message.photo[-1].file_id
    )


@staffRouter.message(StateFilter(AdminState.get_item_description))
async def proceed_item_description(message: Message, state: FSMContext):
    msg = (await state.get_data())["msg"]
    await state.set_state(AdminState.get_item_price)

    await message.delete()
    await msg.edit_text(
        "Пришлите цену товара",
        reply_markup=admin_cancel_kb(),
    )
    await state.update_data(msg=msg, description=message.text)


@staffRouter.message(StateFilter(AdminState.get_item_price))
async def proceed_item_price(message: Message, state: FSMContext, api: ApiWrapper):
    try:
        price = int(message.text)
    except ValueError:
        await message.answer("Пришлите число")

    data = await state.get_data()
    msg = data["msg"]
    del data["msg"]

    await message.delete()
    await api.create_item(
        name=data["name"],
        price=price,
        description=data["description"],
        photo=data["photo"],
        category_id=data["category_id"],
    )
    await state.clear()
    await msg.edit_text("✅ Товар успешно добавлен", reply_markup=admin_back_kb())


@staffRouter.callback_query(F.data.startswith("admin_update_item"))
async def update_item_manager(call: CallbackQuery, state: FSMContext):
    item_id = int(call.data.split("_")[-1])
    update_type = call.data.split("_")[-2]
    await state.set_state(AdminState.get_update_data)
    await state.update_data(msg=call.message, item_id=item_id, update_type=update_type)
    await call.message.answer("Пришлите новые данные")


@staffRouter.message(StateFilter(AdminState.get_update_data))
async def update_item_data(message: Message, state: FSMContext, api: ApiWrapper):
    data = await state.get_data()
    msg = data["msg"]
    item_id = data["item_id"]
    update_type = data["update_type"]

    data = (
        message.photo[-1].file_id
        if message.photo
        else (int(message.text) if update_type == "price" else message.text)
    )

    await message.delete()

    await api.update_item(item_id=item_id, update_type=update_type, data=data)

    await msg.delete()
    await message.answer("✅ Товар успешно обновлен", reply_markup=admin_back_kb())

    await state.clear()


@staffRouter.message(F.text.startswith("+admin") | F.text.startswith("-admin"))
async def manage_admin_role(message: Message, api: ApiWrapper):
    user_id = int(message.text.split(" ")[-1])

    if message.from_user.id == user_id:
        await message.delete()
        await message.answer("Вы не можете снять права администратора с себя ❌", reply_markup=admin_back_kb())
        return
    
    await api.update_user_role(
        user_id=user_id, role="admin" if "+admin" in message.text else "user"
    )
    await message.delete()
    await message.answer("Админка обновлена ✅", reply_markup=admin_back_kb())
