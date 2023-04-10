from aiogram.types import CallbackQuery, FSInputFile
from aiogram import F
from yestabak.api_wrapper import ApiWrapper
from yestabak.keyboards import profile_kb
from yestabak.routes import userRouter


def format_profile_info(name: str, address: str = None, payment_method: str = None, **kwargs):
    return f"""
Здравствуйте, {name.capitalize()}!
Адрес: {address if address else 'не указано'}
Оплата: {payment_method if payment_method else 'не указано'} 
"""


@userRouter.callback_query(F.data == 'my_profile')
async def my_profile(call: CallbackQuery, api: ApiWrapper):
    await call.message.delete()
    user = await api.get_user_if_exists(call.from_user.id)
    await call.message.answer_photo(FSInputFile('yestabak/assets/profile.jpg'), caption=format_profile_info(user['user']['first_name'], user['addresses'][0] if len(user['addresses']) else None), reply_markup=profile_kb())
