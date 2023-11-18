import aiosqlite
from aiogram import Bot
from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError
from app.keyboards import reply as kb


async def send_notifications_task(bot: Bot, message: str) -> Message:
    """
    Задача, которая отправляет сообщение(уведомление) о уроках на завтра.
    :param bot: Bot
    :param message: Message
    """
    async with aiosqlite.connect('schoolDiary.db') as db:
        async with db.execute("""SELECT user_id FROM users;""") as cursor:
            async for users in cursor:
                for user in list(users):
                    try:
                        await bot.send_message(user, text=f'{message}', parse_mode='HTML')
                    except TelegramForbiddenError:
                        pass