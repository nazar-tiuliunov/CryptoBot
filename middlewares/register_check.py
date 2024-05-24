from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from db.base import get_user_by_id, create_user


class RegisterCheck(BaseMiddleware):

    def __init__(self):
        pass

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        user = event.from_user
        if get_user_by_id(user.id, con=data['con']) is None:
            create_user(user.id, user.username, user.first_name, con=data['con'])
            await data['bot'].send_message(user.id, 'You are registered!')
        return await handler(event, data)
