"""
Module defining FSM states for adding and selecting favorite currencies.
"""

from aiogram.fsm.state import StatesGroup, State


class AddFavCurrenciesStates(StatesGroup):
    """
        States group for adding favorite currencies.
    """
    waiting_for_enter = State()


class SelectCurrencyStates(StatesGroup):
    """
        States group for selecting currencies.
    """
    waiting_for_select = State()
