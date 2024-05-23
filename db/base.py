import sqlite3


def create_table(con):
    cursor = con.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                portfolio TEXT
            )
        """)
    con.commit()


def create_user(user_id, con):
    cursor = con.cursor()
    cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
    con.commit()


def get_user_by_id(user_id, con):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()


async def get_user_portfolio(user_id, db):
    async with db.cursor() as cursor:
        await cursor.execute("SELECT portfolio FROM users WHERE user_id=?", (user_id,))
        result = await cursor.fetchone()
        return result[0] if result else None


async def set_user_portfolio(user_id, portfolio, db):
    async with db.cursor() as cursor:
        await cursor.execute("INSERT OR REPLACE INTO users (user_id, portfolio) VALUES (?, ?)", (user_id, portfolio))
        await db.commit()
