from aiogram import F
from aiogram.types import Message, CallbackQuery
from yestabak.keyboards.items_builder import admin_items_kb
from yestabak.routes import userRouter
from yestabak.api_wrapper import ApiWrapper
from yestabak.states import AdminState
from yestabak.keyboards import categories_kb


@userRouter.message(F.text == "/admin")
@userRouter.callback_query(F.data == "admin")
async def admin_menu_handler(event: Message | CallbackQuery, api: ApiWrapper):
    categories = await api.get_categories()
    if isinstance(event, Message):
        await event.delete()
        await event.answer(
            "Добро пожаловать в админ-меню. Выберите категорию из списка ниже, чтобы начать с ней взаимодействовать, или создайте новую",
            reply_markup=categories_kb(categories, is_admin_menu=True),
        )
        return
    await event.message.delete()
    await event.message.edit_text(
        "Добро пожаловать в админ-меню. Выберите категорию из списка ниже, чтобы начать с ней взаимодействовать, или создайте новую",
        reply_markup=categories_kb(categories, is_admin_menu=True),
    )


@userRouter.callback_query(F.data.startswith("admin_category"))
async def admin_category_settings(call: CallbackQuery, api: ApiWrapper):
    category_id = int(call.data.split("_")[-1])
    items = await api.get_category_items(category_id)
    await call.message.edit_text(
        "Здесь вы можете добавить/удалить/изменить товар(ы), а также удалить категорию",
        reply_markup=admin_items_kb(items, category_id),
    )
