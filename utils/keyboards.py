"""
Utility functions for creating inline keyboards.
"""

from aiogram import types


def get_main_menu_keyboard():
    """
        Get the main menu keyboard.

        Returns:
            types.InlineKeyboardMarkup: The main menu keyboard.
    """
    kb = [
        [
            types.InlineKeyboardButton(text='👤 My Account', callback_data='my_account'),
        ],
        [
            types.InlineKeyboardButton(text='⭐️ Favorite currencies',
                                       callback_data='favorite_user_list'),
            types.InlineKeyboardButton(text='🔝 Top 50 currencies ',
                                       callback_data='top_list'),
        ],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def get_back_keyboard():
    """
        Get the back keyboard.

        Returns:
            types.InlineKeyboardMarkup: The back keyboard.
    """
    kb = [
        [
            types.InlineKeyboardButton(text='⬅️ Back', callback_data='back'),
        ],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)
