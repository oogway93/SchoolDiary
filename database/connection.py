import aiosqlite


async def create_db() -> None:
    async with aiosqlite.connect('schoolDiary.db') as db:
        if db:
            print("DB was started(created)")
        await db.execute(
            """CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL
            );"""
        )
        await db.commit()
