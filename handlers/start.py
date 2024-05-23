from aiogram import Router, types
from aiogram.filters import CommandStart


async def start_cmd(message: types.Message):
    await message.answer('Hello, world!')
