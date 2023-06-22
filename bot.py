import asyncio
import logging

from aiogram import Bot, Dispatcher
from handlers import start_handler
from config import TOKEN

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    logging.basicConfig(level=logging.INFO)
    dp.include_router(start_handler.router_start)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
