import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message

from config import API_TOKEN

bot = Bot(API_TOKEN, parse_mode='HTML')

dp = Dispatcher()


def on_startup() -> str:
    print("Bot was started")


@dp.message()
async def handler(message: Message) -> Message:
    await message.reply("HEllo")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, on_startup=on_startup())


if __name__ == '__main__':
    asyncio.run(main())
