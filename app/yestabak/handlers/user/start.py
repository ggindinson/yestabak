from typing import Union
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import (
    Message,
    CallbackQuery,
    InputMediaPhoto,
)
from aiogram.fsm.context import FSMContext
from yestabak.api_wrapper import ApiWrapper
from yestabak.configs.config import MENU_IMAGE
from yestabak.routes.user.router import userRouter
from yestabak.keyboards import start_menu_kb, contact_kb
from yestabak.states import RegState


# To handle photos and send their "file_id" attribute (to reuse without downloading again and again)
@userRouter.message(F.photo)
async def photo_handler(message: Message):
    await message.reply(message.photo[-1].file_id)


@userRouter.message(F.text == "/start", StateFilter("*"))
@userRouter.callback_query(F.data == "main_menu", StateFilter("*"))
async def start_handler(
    message: Union[Message, CallbackQuery], state: FSMContext, api: ApiWrapper
):
    # await state.clear()
    if isinstance(message, CallbackQuery):
        message = message.message
    else:
        user = await api.get_user_if_exists(message.from_user.id)

        if not user:
            await state.set_state(RegState.get_first_name)
            msg = await message.answer(
                "<b><i>Регистрация (шаг 1/3)</i></b>\n\n<b>Пришлите свое имя</b>",
            )
            await state.update_data(msg=msg)
            return

    if message.photo:
        await message.edit_media(
            InputMediaPhoto(
                media=MENU_IMAGE,
                caption="<b>Добро пожаловать!</b>",
            ),
            reply_markup=start_menu_kb(),
        )
    else:
        await message.answer_photo(
            photo=MENU_IMAGE,
            caption="<b>Добро пожаловать!</b>",
            reply_markup=start_menu_kb(),
        )


@userRouter.message(StateFilter(RegState.get_first_name))
async def get_user_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(RegState.get_last_name)

    msg: Message = (await state.get_data())["msg"]
    await message.delete()
    await msg.edit_text(
        "<b><i>Регистрация (шаг 2/3)</i></b>\n\n<b>Пришлите свою фамилию</b>",
    )


@userRouter.message(StateFilter(RegState.get_last_name))
async def get_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(RegState.get_phone)

    msg: Message = (await state.get_data())["msg"]
    await message.delete()
    await msg.delete()

    msg = await message.answer(
        "<b><i>Регистрация (шаг 3/3)</i>\n\nПришлите свой номер телефона</b>",
        reply_markup=contact_kb(),
    )

    await state.update_data(msg=msg)


@userRouter.message(StateFilter(RegState.get_phone))
async def get_phone(message: Message, state: FSMContext, api: ApiWrapper):
    data = await state.get_data()
    msg: Message = data["msg"]
    del data["msg"]

    await api.create_user(
        phone_number=message.text or message.contact.phone_number,
        telegram_id=message.from_user.id,
        username=message.from_user.username if message.from_user.username else None,
        **data
    )

    await state.clear()
    await message.delete()
    await msg.delete()
    await message.answer(text="<b>Спасибо за регистрацию!</b> \n<i>Теперь вы можете пользоваться нашим ботом!</i>", reply_markup=None)
    await start_handler(message, state, api)
