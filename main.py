import asyncio
import logging
import sqlite3

import os
from aiogram import Bot, Dispatcher
from binance.client import Client

from db.base import create_table, get_connection
from handlers import register_handlers, callback_handler


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    client = Client(api_key=os.getenv('BINANCE_API_KEY'),
                    api_secret=os.getenv('BINANCE_SECRET_KEY'))
    con = sqlite3.connect("database.db")

    create_table(get_connection())

    register_handlers(dp)
    callback_handler(dp)

    await dp.start_polling(bot, skip_updates=True, con=con, client=client)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
