import logging

import aiosqlite
from aiosqlite import IntegrityError
from pymongo import MongoClient
from config import MONGO_url


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


cluster = MongoClient(MONGO_url)
db = cluster['ScheduleDB']
collection = db['Schedule']


def update_schedule(class_name: str, day: str, new_schedule: str):
    collection.update_one({"class_name": class_name}, {"$set": {f"schedule.{day}": new_schedule.split('\n')}})
