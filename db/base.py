import sqlite3


def create_table(con):
    cursor = con.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username VARCHAR(32),
                user_first_name VARCHAR(32),
                selected_pairs TEXT,
                favorite_pair TEXT,
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
