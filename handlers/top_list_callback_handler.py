from aiogram import Router, types, F

from services import get_top_list
from utils.keyboards import get_back_keyboard

router = Router()


@router.callback_query(F.data == 'top_list')
async def get_top_list_currency(callback: types.CallbackQuery):
    top_50 = get_top_list.main()
    kb = get_back_keyboard()
    await callback.message.edit_text(top_50, reply_markup=kb)
