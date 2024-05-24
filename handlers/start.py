from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import utils


async def start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    user_first_name = message.from_user.first_name
    kb = utils.keyboards.get_main_menu_keyboard()
    await message.answer(f"Hi, {user_first_name}! You are in main menu: ", reply_markup=kb)
