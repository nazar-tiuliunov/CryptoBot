"""
This script is responsible for running the Telegram bot.
"""
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher

from db.base import create_table, get_connection
from handlers import (start_handler,
                      callback_handler,
                      user_profile_callback_handler,
                      top_list_callback_handler,
                      forever_currency_list_callback_handler)
from services.binance_api import get_client


async def main():
    """
        Main function to start the bot.

        Sets up logging configuration, initializes the bot and dispatcher,
        creates a connection to the database, gets the Binance client,
        creates necessary tables in the database, includes required handlers,
        and starts the bot to receive updates.

        Raises:
            Exception: If an error occurs during execution.
    """
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    con = get_connection()
    client = await get_client()

    create_table(get_connection())

    dp.include_routers(start_handler.router,
                       callback_handler.router,
                       user_profile_callback_handler.router,
                       top_list_callback_handler.router,
                       forever_currency_list_callback_handler.router)

    await dp.start_polling(bot, skip_updates=True, con=con, client=client)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
