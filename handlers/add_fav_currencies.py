from aiogram import types
from aiogram.fsm.context import FSMContext

from db.base import set_favorite_pairs, get_connection
from states.states import AddFavCurrenciesStates
from utils.keyboards import get_back_keyboard
from aiogram_dialog import DialogManager, StartMode


async def func_add_fav_curr(callback: types.CallbackQuery, state: FSMContext):
    kb = get_back_keyboard()
    await callback.message.edit_text(f"Enter your favorite currency pairs separated by commas \n\n "
                                     f"Example: BTC, ETH, ADA, XRP, LTC \n\n"
                                     f"You can enter up to 5 pairs.", reply_markup=kb)
    await state.set_state(AddFavCurrenciesStates.waiting_for_enter)


async def func_enter_fav_curr(message: types.Message, state: FSMContext):
    text = message.text
    pairs = text.split(',')
    pairs = [x.strip().upper() for x in pairs]
    pairs = pairs[:5]
    set_favorite_pairs(message.from_user.id, text, get_connection())
    kb = [
        [types.InlineKeyboardButton(text='Add another', callback_data='add_fav_pairs')],
        [types.InlineKeyboardButton(text='View list', callback_data='view_fav_pairs')],
        [types.InlineKeyboardButton(text='⬅️ Back', callback_data='back')],
    ]
    await message.answer(f'You have entered the following favorite currency pairs: {text}',
                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))
    await state.clear()
