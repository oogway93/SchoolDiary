import aiosqlite


async def create_db() -> None:
    async with aiosqlite.connect('schoolDiary.db') as db:
        if db:
            print("DB was started(created)")
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
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS Schedule
            (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id   INTEGER NOT NULL,
                day_id     INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                FOREIGN KEY (class_id) REFERENCES Class (class_id),
                FOREIGN KEY (day_id) REFERENCES Day (day_id),
                FOREIGN KEY (subject_id) REFERENCES Subject (subject_id)
            );
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS Class
            (
                class_id INTEGER PRIMARY KEY AUTOINCREMENT,
                class    VARCHAR(3) UNIQUE NOT NULL
            );
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS Day
            (
                day_id INTEGER PRIMARY KEY AUTOINCREMENT,
                day    VARCHAR(30) NOT NULL
            );
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS Subject
            (
                subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject    VARCHAR(50) NOT NULL UNIQUE
            );
            """
        )
        await db.commit()
