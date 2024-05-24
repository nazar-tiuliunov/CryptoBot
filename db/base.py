import sqlite3


def get_connection():
    return sqlite3.connect('database.db')


def create_table(con):
    cursor = con.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username VARCHAR(32),
                user_first_name VARCHAR(32),
                favorite_pairs TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    con.commit()


def create_user(user_id, username, user_first_name, con):
    cursor = con.cursor()
    cursor.execute("INSERT INTO users (user_id, username, user_first_name) VALUES (?, ?, ?)",
                   (user_id, username, user_first_name))
    con.commit()


def get_user_by_id(user_id, con):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()


def get_favorite_pairs(user_id, con):
    cursor = con.cursor()
    cursor.execute("SELECT favorite_pairs FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None


def set_favorite_pairs(user_id, favorite_pairs, con):
    cursor = con.cursor()
    cursor.execute("UPDATE users SET favorite_pairs=? WHERE user_id=?", (favorite_pairs, user_id))
    con.commit()
