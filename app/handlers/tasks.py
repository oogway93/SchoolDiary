import aiosqlite
from aiogram import Bot
from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError


async def send_notifications_18_task(bot: Bot, message: str, user_id) -> Message:
    """
    Задача, которая отправляет сообщение(уведомление) об уроках в 18:00 на завтра.
    :param user_id:
    :param bot: Bot
    :param message: Message
    """
    try:
        await bot.send_message(user_id, text=f'Ваше на расписание на завтра: \n\n{message}', parse_mode='HTML')
    except TelegramForbiddenError:
        pass


async def send_notifications_7_task(bot: Bot, message: str, user_id) -> Message:
    """
    Задача, которая отправляет сообщение(уведомление) об уроках в 7:00 текущего дня .
    :param user_id:
    :param bot: Bot
    :param message: Message
    """
    try:
        await bot.send_message(user_id, text=f'Ваше на расписание на сегодня: \n\n{message}', parse_mode='HTML')
    except TelegramForbiddenError:
        pass


async def send_message_admin(bot: Bot, message: Message):
    async with aiosqlite.connect('schoolDiary.db') as db:
        async with db.execute("""SELECT user_id FROM users;""") as cursor:
            async for users in cursor:
                for user in users:
                    try:
                        await bot.send_message(user, text=f'{message}',
                                               parse_mode='HTML')
                    except TelegramForbiddenError:
                        pass
