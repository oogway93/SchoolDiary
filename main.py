import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import API_TOKEN
from handlers.handlers import router, noon_print
from database import connection

# from handlers.tasks import scheduler

bot = Bot(API_TOKEN, parse_mode='HTML')

dp = Dispatcher()


def on_startup() -> str:
    print("Bot was started")


scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
scheduler.add_job(noon_print, 'cron', day_of_week='mon-sat', hour=23, minute=16)


# scheduler.add_job(noon_print, 'interval', seconds=5)


async def main():
    dp.include_router(router)
    scheduler.start()
    await connection.create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, on_startup=on_startup)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
