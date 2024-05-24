__all__ = ['register_handlers', 'callback_handler']

from aiogram import Router
from aiogram.filters import CommandStart

from middlewares.register_check import RegisterCheck
from .callback_handler import func_fav_currencies, func_top_50, func_my_account, to_back
from .start import start_cmd


def register_handlers(router: Router):
    router.message.register(start_cmd, CommandStart())

    router.message.middleware(RegisterCheck())
    router.callback_query.middleware(RegisterCheck())


def callback_handler(router: Router):
    router.callback_query.register(func_my_account, lambda c: c.data == 'my_account')
    router.callback_query.register(func_fav_currencies, lambda c: c.data == 'fav_currencies')
    router.callback_query.register(func_top_50, lambda c: c.data == 'top_50')
    router.callback_query.register(to_back, lambda c: c.data == 'back')
