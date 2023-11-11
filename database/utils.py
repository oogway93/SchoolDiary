import aiosqlite
from aiogram import Bot
from aiogram.types import Message
from aiosqlite import IntegrityError


async def insert_user_sql(user_id: int, username: str) -> None:
    """Вставить user id в базу данных"""
    async with aiosqlite.connect('schoolDiary.db') as db:
        async with db.execute("""SELECT * FROM users;""") as cursor:
            try:
                query = await cursor.execute("""SELECT NOT EXISTS(SELECT * FROM users WHERE user_id=?)""", (user_id,))
                if query:
                    await cursor.execute("""INSERT INTO users(user_id, username) VALUES(?, ?);""", (user_id, username))
                    await db.commit()
            except IntegrityError:
                raise IntegrityError('Этот пользователь уже записан в базу данных')


async def send_notifications_task(bot: Bot, message: str) -> Message:
    async with aiosqlite.connect('schoolDiary.db') as db:
        async with db.execute("""SELECT user_id FROM users;""") as cursor:
            async for users in cursor:
                for user in list(users):
                    await bot.send_message(user, text=f'{message}', parse_mode='HTML')
