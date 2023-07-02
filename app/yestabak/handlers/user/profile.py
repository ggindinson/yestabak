from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message
from aiogram import F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from typing import Literal
from yestabak.api_wrapper import ApiWrapper
from yestabak.keyboards import (
    profile_kb,
    addresses_kb,
    edit_address_kb,
    cancel_address_kb,
)
from yestabak.routes import userRouter
from yestabak.states import AddressState


def format_profile_info(
    name: str, last_name: str, step: Literal["cart", "addresses", "orders"]
):
    steps_alias = {
        "menu": "Управляйте своими данными",
        "addresses": "Управляйте своими адресами",
        "cart": "Просмотрите свои покупки",
    }

    return f"""
Здравствуйте, {name.capitalize()} {last_name.capitalize()}!
{steps_alias[step]} 😉
"""


@userRouter.callback_query(F.data == "my_profile")
async def my_profile(call: CallbackQuery, api: ApiWrapper):
    user = await api.get_user_if_exists(call.from_user.id)
    await call.message.edit_media(
        InputMediaPhoto(
            media=FSInputFile("yestabak/assets/profile.jpg"),
            caption=format_profile_info(
                user.user.first_name, user.user.last_name, step="menu"
            ),
        ),
        reply_markup=profile_kb(),
    )


@userRouter.callback_query(F.data == "my_addresses", StateFilter("*"))
async def my_addresses(
    event: CallbackQuery | Message, api: ApiWrapper, state: FSMContext
):
    user_id = event.from_user.id
    user = await api.get_user_if_exists(user_id)
    if isinstance(event, CallbackQuery):
        try:
            await event.message.edit_media(
                media=InputMediaPhoto(
                    media=FSInputFile("yestabak/assets/addresses.jpg"),
                    caption=format_profile_info(
                        user.user.first_name,
                        user.user.last_name,
                        step="addresses",
                    ),
                ),
                reply_markup=addresses_kb(user.addresses),
            )
        except:
            await event.message.delete()
            await event.message.answer_photo(
                FSInputFile("yestabak/assets/profile.jpg"),
                caption=format_profile_info(
                    user.user.first_name,
                    user.user.last_name,
                    step="addresses",
                ),
                reply_markup=addresses_kb(user.addresses),
            )
    else:
        await event.answer_photo(
            FSInputFile("yestabak/assets/profile.jpg"),
            caption=format_profile_info(
                user.user.first_name, user.user.last_name, step="menu"
            ),
            reply_markup=profile_kb(),
        )
    # We are caching all user addresses to optimise getting single one in another handlers
    await state.set_state(AddressState.menu)
    await state.update_data(addresses=user.addresses)


@userRouter.callback_query(
    F.data.contains("address_additional_"), StateFilter(AddressState.menu)
)
async def address_additional_info(call: CallbackQuery, state: FSMContext):
    address_id = int(call.data.split("_")[-1])
    all_addresses = (await state.get_data())["addresses"]
    current_address = list(
        filter(lambda address: address.id == address_id, all_addresses)
    )[0]

    await call.message.edit_caption(
        caption=f"Название адреса: {current_address.data['name']}\n\nПолный адрес: <i><b>{current_address.data['address']}</b></i>",
        reply_markup=edit_address_kb(address_id),
    )


@userRouter.callback_query(
    F.data.contains("delete_address_") | F.data.contains("add_address")
)
async def address_edit_manager(call: CallbackQuery, state: FSMContext, api: ApiWrapper):
    if "delete_address" in call.data:
        address_id = int(call.data.split("_")[-1])
        await api.delete_user_address(address_id)
        await call.answer("Адрес удален ✅", show_alert=True)
        return await my_addresses(call, api, state)
    else:
        await call.message.delete()
        msg = await call.message.answer(
            'Пришлите название адреса (например, "Мой дом") \n\nНикто кроме вас не будет видеть эту информацию!',
            reply_markup=cancel_address_kb(),
        )
        await state.clear()
        await state.set_state(AddressState.get_name)
        await state.update_data(message_id=msg.message_id)


@userRouter.message(StateFilter(AddressState.get_name))
async def address_name_handler(message: Message, state: FSMContext, bot: Bot):
    message_id = (await state.get_data())["message_id"]
    await bot.edit_message_text(
        text="Пришлите адрес текстом.\nПример: Улица Пушкина, дом 2",
        message_id=message_id,
        chat_id=message.from_user.id,
        reply_markup=cancel_address_kb(),
    )
    await message.delete()
    await state.set_state(AddressState.get_address)
    await state.update_data(name=message.text)


@userRouter.message(StateFilter(AddressState.get_address))
async def address_data_handler(
    message: Message, state: FSMContext, api: ApiWrapper, bot: Bot
):
    data = await state.get_data()
    message_id = (await state.get_data())["message_id"]
    await api.create_user_address(
        address={
            "data": {"address": message.text, "name": data["name"]},
            "telegram_id": message.from_user.id,
        },
    )
    await message.delete()
    await bot.delete_message(message_id=message_id, chat_id=message.from_user.id)
    await my_addresses(message, api, state)
