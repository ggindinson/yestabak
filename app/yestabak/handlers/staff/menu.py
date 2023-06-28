from aiogram import F
from aiogram.types import Message, CallbackQuery, URLInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from yestabak.keyboards.items_builder import (
    admin_item_settings_kb,
    admin_back_kb,
    admin_items_kb,
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
        else InputMediaPhoto(media=item["photo"]),
        caption="Здесь вы можете отредактировать/удалить товар",
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
