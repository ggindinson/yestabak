import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery
from aiogram.fsm.context import FSMContext
from typing import Callable, Dict, Any, Awaitable

from yestabak.api_wrapper import ApiWrapper

logger = logging.getLogger()


class TransferCartDataMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        call: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        state: FSMContext = data["state"]
        api: ApiWrapper = data["api"]
        current_state = await state.get_state()
        if "item" in call.data or current_state not in [
            "CategoryState:menu",
            "CartState:cart",
        ]:
            return await handler(call, data)
        
        cart = (await state.get_data()).get("cart", [])

        for row in cart:
            try:
                row["item_id"] = row.pop("id")
            except Exception as err:
                print("Error in cart middleware:", err)
                break
            
        logger.info(f"Local cart: {cart}")

        await api.post_cart(user_id=call.from_user.id, cart=cart)
        return await handler(call, data)
