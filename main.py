import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import API_TOKEN
from app.handlers import (
    handlers,
    unexpected
)
from app.admin import admin
from app.database import connection

bot = Bot(API_TOKEN, parse_mode='HTML')

dp = Dispatcher()


def on_startup() -> str:
    print("Bot was started")


scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
scheduler.add_job(handlers.send_notifications_each_day_18_handler, 'cron', day_of_week='mon-sun', hour=18, minute=0,
                  kwargs={'bot': bot})

scheduler.add_job(handlers.send_notifications_each_day_7_handler, 'cron', day_of_week='mon-sun', hour=7, minute=0,
                  kwargs={'bot': bot})


async def main():
    dp.include_router(handlers.router)
    dp.include_router(admin.router)
    dp.include_router(unexpected.router)
    scheduler.start()
    await connection.create_db_sqlite()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, on_startup=on_startup)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                        format="%(name)s : %(asctime)s : %(levelname)s : %(message)s")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
