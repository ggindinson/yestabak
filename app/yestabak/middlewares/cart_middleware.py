from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import TelegramObject, CallbackQuery
from aiogram.fsm.context import FSMContext
from yestabak.api_wrapper import ApiWrapper


class TransferCartDataMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        call: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        if "item" not in call.data:
            state: FSMContext = data["state"]
            api: ApiWrapper = data["api"]
            current_state = await state.get_state()
            if current_state and current_state == "CategoryState:menu":
                cart = (await state.get_data())["cart"]
                if len(cart):
                    await api.post_cart(user_id=call.from_user.id, cart=cart)
        return await handler(call, data)
