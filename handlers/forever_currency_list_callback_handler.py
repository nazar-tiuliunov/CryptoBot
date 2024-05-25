"""
Module containing routes and callback handlers for working with favorite currency pairs.
"""

import re

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.binance_api import get_info_currency
from services.service_forever_currency import (get_forever_list,
                                               send_request_for_add_new_pair,
                                               send_request_for_delete_pair)
from states.states import AddFavCurrenciesStates

router = Router()


@router.callback_query(F.data == 'favorite_user_list')
async def forever_currency_list(callback: types.CallbackQuery):
    """
        Callback handler to display the list of favorite currency pairs for a user.

        Args:
            callback (types.CallbackQuery): The callback query triggering the handler.

        Returns:
            None
    """
    pairs = get_forever_list(callback.from_user.id)
    builder = InlineKeyboardBuilder()
    if pairs:
        for pair in pairs:
            button = InlineKeyboardButton(text=pair[0], callback_data=f"fav_currency:{pair[0]}")
            builder.row(button)
    builder.row(InlineKeyboardButton(text='Add favorite pairs', callback_data='add_favorite_pairs'))
    builder.row(InlineKeyboardButton(text='⬅️ Back', callback_data='back'))
    await callback.message.edit_text('Favorite currencies', reply_markup=builder.as_markup())


@router.callback_query(F.data == 'add_favorite_pairs')
async def add_favorite_pairs(callback: types.CallbackQuery, state: FSMContext):
    """
        Callback handler to initiate adding a new favorite currency pair.

        Args:
            callback (types.CallbackQuery): The callback query triggering the handler.
            state (FSMContext): The FSM context.

        Returns:
            None
    """
    await callback.message.edit_text("Enter the currency pair you want to add\n\n"
                                     "(e.g. BTC, or ETH, etc.)")
    await state.set_state(AddFavCurrenciesStates.waiting_for_enter)


@router.callback_query(F.data == 'delete_currency')
async def delete_currency(callback: types.CallbackQuery, state: FSMContext):
    """
        Callback handler to delete a favorite currency pair.

        Args:
            callback (types.CallbackQuery): The callback query triggering the handler.
            state (FSMContext): The FSM context.

        Returns:
            None
    """
    user_data = await state.get_data()
    result = send_request_for_delete_pair(callback.from_user.id, user_data.get('symbol'))
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='View favorite list', callback_data='favorite_user_list'))
    builder.row(InlineKeyboardButton(text='Main menu', callback_data='back'))
    if result is True:
        await callback.message.edit_text('Currency deleted successfully!', reply_markup=builder.as_markup())
    else:
        await callback.message.edit_text('Error occurred while deleting currency!',
                                         reply_markup=builder.as_markup())


@router.message(AddFavCurrenciesStates.waiting_for_enter)
async def process_add_favorite_currency_request(message: types.Message, state: FSMContext):
    """
        Handler to process the request to add a new favorite currency pair.

        Args:
            message (types.Message): The message containing the user's input.
            state (FSMContext): The FSM context.

        Returns:
            None
    """
    if re.match(r'^[A-Z]{2,4}$', message.text) is None:
        await message.answer('Invalid currency pair! Please, try again')
        await state.set_state(AddFavCurrenciesStates.waiting_for_enter)
        return None
    result = send_request_for_add_new_pair(message.from_user.id, message.text)
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='View favorite list', callback_data='favorite_user_list'))
    builder.row(InlineKeyboardButton(text='Add new pair', callback_data='add_favorite_pairs'))
    builder.row(InlineKeyboardButton(text='Main menu', callback_data='back'))
    if result is True:
        await message.answer('Currency pair added successfully!', reply_markup=builder.as_markup())
    else:
        await message.answer('Currency pair already exists!', reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith('fav_currency:'))
async def forever_currency_description(callback: types.CallbackQuery, state: FSMContext):
    """
        Callback handler to display information about a specific favorite currency pair.

        Args:
            callback (types.CallbackQuery): The callback query triggering the handler.
            state (FSMContext): The FSM context.

        Returns:
            None
    """
    symbol = callback.data.split(':')[1]
    await state.set_data({"symbol": symbol})
    print(symbol)
    try:
        result = await get_info_currency(symbol)
    except Exception as e:
        print(e)
        result = None
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Delete this currency', callback_data='delete_currency'))
    builder.row(InlineKeyboardButton(text='Back to favorite list', callback_data='favorite_user_list'))
    builder.row(InlineKeyboardButton(text='Main menu', callback_data='back'))
    if result is not None:
        await callback.message.edit_text(f"Currency: {symbol}\n\n"
                                         f"Price: {result[1]}$", reply_markup=builder.as_markup())
    else:
        await callback.message.edit_text('Error occurred while getting currency info. Currency is incorrect!',
                                         reply_markup=builder.as_markup())
