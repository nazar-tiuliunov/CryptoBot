import asyncio
import logging
import sqlite3

from aiogram import Bot, Dispatcher
from binance.client import Client
import os

from db.base import create_table
from handlers import register_handlers


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    client = Client(api_key=os.getenv('BINANCE_API_KEY'), api_secret=os.getenv('BINANCE_SECRET_KEY'))
    con = sqlite3.connect("database.db")

    create_table(con)
    register_handlers(dp)

    await dp.start_polling(bot, skip_updates=True, con=con, client=client)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
