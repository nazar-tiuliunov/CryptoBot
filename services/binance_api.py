import os
from binance import AsyncClient, Client


async def get_client():
    client = Client(api_key=os.getenv('BINANCE_API_KEY'), api_secret=os.getenv('BINANCE_SECRET_KEY'))
    return client


async def get_account_info():
    client = await get_client()
    account_info = client.get_account()
    return account_info


async def get_info_currency(symbol):
    client = await AsyncClient.create()
    info = await client.get_exchange_info()
    ticker = await client.get_ticker(symbol=symbol + 'USDT')
    try:
        symbol_info = next(item for item in info['symbols'] if item['symbol'] == symbol + 'USDT')
    except StopIteration:
        symbol_info = None
    await client.close_connection()
    return symbol_info, ticker['lastPrice']
