from aiogram.fsm.state import StatesGroup, State


class AddFavCurrenciesStates(StatesGroup):
    waiting_for_enter = State()
