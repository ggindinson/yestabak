from typing import Union
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from yestabak.api_wrapper import ApiWrapper
from yestabak.routes.user.router import userRouter
from yestabak.keyboards import start_menu_kb, contact_kb
from yestabak.states import RegState


@userRouter.message(F.text == "/start", StateFilter("*"))
@userRouter.callback_query(F.data == "main_menu", StateFilter("*"))
async def start_handler(
    message: Union[Message, CallbackQuery], state: FSMContext, api: ApiWrapper
):
    await state.clear()

    user_id = message.from_user.id

    if isinstance(message, CallbackQuery):
        message = message.message
        await message.delete()

    user = await api.get_user_if_exists(user_id)
    if not user:
        await state.set_state(RegState.get_first_name)
        sent_msg = await message.answer(
            "<b><i>Регистрация (шаг 1/3)</i></b>\n\n<b>Пришлите свое имя</b>"
        )
        await state.update_data(msg=sent_msg)
        return

    await message.answer_photo(
        photo=FSInputFile("yestabak/assets/menu.jpg"),
        caption="<b>Добро пожаловать!</b>",
        reply_markup=start_menu_kb(),
    )


@userRouter.message(StateFilter(RegState.get_first_name))
async def get_user_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(RegState.get_last_name)

    msg = (await state.get_data())["msg"]
    await message.delete()
    await msg.edit_text(
        "<b><i>Регистрация (шаг 2/3)</i></b>\n\n<b>Пришлите свою фамилию</b>"
    )


@userRouter.message(StateFilter(RegState.get_last_name))
async def get_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(RegState.get_phone)

    msg = (await state.get_data())["msg"]
    await message.delete()
    await msg.delete()
    await message.answer(
        "<b><i>Регистрация (шаг 3/3)</i></b>\n\n<b>Пришлите свой номер телефона</b>",
        reply_markup=contact_kb(),
    )


@userRouter.message(StateFilter(RegState.get_phone))
async def get_phone(message: Message, state: FSMContext, api: ApiWrapper):
    data = await state.get_data()
    del data["msg"]
    await message.edit_reply_markup(reply_markup=None)
    await api.create_user(
        phone=message.contact.phone_number or message.text,
        user_id=message.from_user.id,
        username=message.from_user.username,
        **data
    )

    await state.clear()
    await message.delete()
    await start_handler(message, state, api)
