"""
Module containing a router and callback handler.
"""

from aiogram import Router, F, types
from utils import get_main_menu_keyboard

router = Router()


@router.callback_query(F.data == 'back')
async def to_back(callback: types.CallbackQuery):
    """
        Callback handler to navigate back to the main menu.

        Args:
            callback (types.CallbackQuery): The callback query triggering the handler.
    """
    user_first_name = callback.from_user.first_name
    kb = get_main_menu_keyboard()
    await callback.message.edit_text(f"Hi, {user_first_name}! You are in main menu: ", reply_markup=kb)
