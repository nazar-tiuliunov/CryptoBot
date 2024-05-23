__all__ = ['register_handlers']

from aiogram import Router
from aiogram.filters import CommandStart

from middlewares.register_check import RegisterCheck
from .start import start_cmd


def register_handlers(router: Router):
    router.message.register(start_cmd, CommandStart())

    router.message.middleware(RegisterCheck())
