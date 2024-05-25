"""
Module containing functions for interacting with the Binance API asynchronously.
"""

import asyncio
import os
from binance import AsyncClient, Client


async def get_client():
    """
        Asynchronously create and return a Binance client instance.

        Returns:
            Client: The Binance client instance.
    """
    client = Client(api_key=os.getenv('BINANCE_API_KEY'),
                    api_secret=os.getenv('BINANCE_SECRET_KEY'))
    print(client)
    return client


async def get_account_info():
    """
        Asynchronously retrieve account information from Binance.

        Returns:
            dict: Account information.
    """
    client = await get_client()
    account_info = await client.get_account()
    return account_info


async def get_info_currency(symbol):
    """
        Asynchronously retrieve information for a specific cryptocurrency from Binance.

        Args:
            symbol (str): The symbol of the cryptocurrency.

        Returns:
            tuple: A tuple containing the symbol information dictionary
            and the last price of the cryptocurrency.
    """
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
