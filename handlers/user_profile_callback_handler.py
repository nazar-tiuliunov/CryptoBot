from aiogram import types, Router, F

from services.binance_api import get_account_info, get_client, get_info_currency
from utils.keyboards import get_back_keyboard

router = Router()


@router.callback_query(F.data == 'my_account')
async def user_profile(callback: types.CallbackQuery):
    client = await get_client()
    info = await get_account_info()
    msg_text = ""
    for balance in info['balances']:
        if float(balance['free']) > 0:
            balance = client.get_asset_balance(asset=balance['asset'])
            assets_price = await get_info_currency(balance['asset'])
            msg_text += (f"Currency: {balance['asset']}, Quantity: {balance['free']}, "
                         f"Cost: {float(balance['free']) * float(assets_price[1])}$\n\n")
    kb = get_back_keyboard()
    await callback.message.edit_text(f"My Account:\n\n{msg_text}", reply_markup=kb)
