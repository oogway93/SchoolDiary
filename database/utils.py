import logging

import aiosqlite
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
                logging.info('!!!ЭТОТ ПОЛЬЗОВАТЕЛЬ УЖЕ ЗАПИСАН В БАЗУ ДАННЫХ!!!')
