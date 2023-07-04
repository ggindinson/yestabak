from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from typing import Callable, Dict, Any, Awaitable

from yestabak.api_wrapper import ApiWrapper


class AdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery | Message,
        data: Dict[str, Any],
    ) -> Any:
        api: ApiWrapper = data["api"]
        user = await api.get_user_if_exists(event.from_user.id)
        if user.user.role == "admin":
            return await handler(event, data)
