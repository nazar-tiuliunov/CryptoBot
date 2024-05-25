import asyncio
import os
from binance import AsyncClient, Client


async def get_client():
    client = Client(api_key=os.getenv('BINANCE_API_KEY'), api_secret=os.getenv('BINANCE_SECRET_KEY'))
    print(client)
    return client


async def get_account_info():
    client = await get_client()
    account_info = await client.get_account()
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
    print(symbol_info, ticker['lastPrice'])
    return symbol_info, ticker['lastPrice']


if __name__ == '__main__':
    asyncio.run(get_info_currency('BTC'))
