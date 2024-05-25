"""
Module containing routes and handlers for retrieving the top 50 list of cryptocurrencies.
"""

from aiogram import Router, types, F

from services import get_top_list
from utils.keyboards import get_back_keyboard

router = Router()


@router.callback_query(F.data == 'top_list')
async def get_top_list_currency(callback: types.CallbackQuery):
    """
        Callback handler to retrieve and display the top 50 list of cryptocurrencies.

        Args:
            callback (types.CallbackQuery): The callback query triggering the handler.

        Returns:
            None
    """
    top_50 = get_top_list.main()
    kb = get_back_keyboard()
    await callback.message.edit_text(top_50, reply_markup=kb)
