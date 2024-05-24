from aiogram import Router, types
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

import utils
from middlewares.register_check import RegisterCheck

router = Router()
router.message.middleware(RegisterCheck())
router.callback_query.middleware(RegisterCheck())


@router.message(StateFilter(None), CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    user_first_name = message.from_user.first_name
    kb = utils.keyboards.get_main_menu_keyboard()
    await message.answer(f"Hi, {user_first_name}! You are in main menu: ", reply_markup=kb)
