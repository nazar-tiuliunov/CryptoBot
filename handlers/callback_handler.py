from typing import Dict, Any

import requests
from aiogram import types

from db.base import get_favorite_pairs, get_connection
from utils import get_main_menu_keyboard
from utils.keyboards import get_back_keyboard


async def func_my_account(message: types.Message):
    kb = get_back_keyboard()
    await message.message.edit_text('My Account', reply_markup=kb)


async def func_fav_currencies(callback: types.CallbackQuery):
    fav_pairs = get_favorite_pairs(callback.from_user.id, con=get_connection())
    if fav_pairs is None:
        kb = [
            [types.InlineKeyboardButton(text='Add favorite currencies', callback_data='back')],
            [types.InlineKeyboardButton(text='⬅️ Back', callback_data='back')],
        ]
        await callback.message.edit_text('You have not added any favorite currencies yet!',
                                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))
        return
    kb = get_back_keyboard()
    await callback.message.edit_text('Favorite currencies', reply_markup=kb)


async def func_top_50(callback: types.CallbackQuery):
    url = 'https://api.binance.com/api/v3/ticker/24hr'
    response = requests.get(url)
    data = response.json()

    usdt_pairs = [x for x in data if x['symbol'].endswith('USDT')]
    usdt_pairs = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
    usdt_pairs = [f"{i + 1}. {x['symbol']} - Price: {x['askPrice']} USDT, Change in 24h: {x['priceChangePercent']}%" for
                  i, x in enumerate(usdt_pairs)][:50]
    top_50 = '\n'.join(usdt_pairs)

    kb = get_back_keyboard()

    await callback.message.edit_text(top_50, reply_markup=kb)


async def to_back(callback: types.CallbackQuery):
    user_first_name = callback.from_user.first_name
    kb = get_main_menu_keyboard()
    await callback.message.edit_text(f"Hi, {user_first_name}! You are in main menu: ", reply_markup=kb)
