"""
Module defining FSM state for adding favorite currencies.
"""

from aiogram.fsm.state import StatesGroup, State


class AddFavCurrenciesStates(StatesGroup):
    """
        State for adding favorite currencies.
    """
    waiting_for_enter = State()
