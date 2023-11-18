import aiosqlite


async def create_db_sqlite() -> None:
    """
    Создание базы данных sqlite3
    """
    async with aiosqlite.connect('schoolDiary.db') as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users
            (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id  INTEGER UNIQUE NOT NULL,
                username TEXT UNIQUE    NOT NULL
            );
            """
        )
