"""
Module containing a middleware for user registration check.
"""

from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from db.base import get_user_by_id, create_user


class RegisterCheck(BaseMiddleware):
    """
        Middleware to check user registration and register them if necessary.
    """
    def __init__(self):
        pass

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        """
            Call method to execute the middleware logic.

            Args:
                handler (Callable[[Message, Dict[str, Any]], Awaitable[Any]]):
                    The handler to call after processing.
                event (Union[Message, CallbackQuery]): The event triggering the middleware.
                data (Dict[str, Any]): Additional data passed to the middleware.

            Returns:
                Any: Result of calling the handler after processing.
        """
        user = event.from_user
        if get_user_by_id(user.id, con=data['con']) is None:
            create_user(user.id, user.username, user.first_name, con=data['con'])
            await data['bot'].send_message(user.id, 'You are registered!')
        return await handler(event, data)
