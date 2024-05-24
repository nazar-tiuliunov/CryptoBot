import sqlite3
import os


def get_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    database = os.path.join(base_dir, 'database.db')
    return sqlite3.connect(database)


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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorite_currencies (
                user_id INTEGER,
                currency_symbol TEXT,
                UNIQUE (user_id, currency_symbol),
                PRIMARY KEY (user_id, currency_symbol),
                FOREIGN KEY (user_id) REFERENCES users (user_id)
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
    cursor.execute("SELECT currency_symbol FROM favorite_currencies WHERE user_id=?", (user_id,))
    result = cursor.fetchall()
    return result if result else None


def add_new_favorite_pair(user_id, currency_symbol, con):
    cursor = con.cursor()
    try:
        cursor.execute("INSERT INTO favorite_currencies (user_id, currency_symbol) VALUES (?, ?)",
                       (user_id, currency_symbol))
        con.commit()
        return True
    except Exception as e:
        return e


def delete_favorite_pair(user_id, currency_symbol, con):
    cursor = con.cursor()
    try:
        cursor.execute("DELETE FROM favorite_currencies WHERE user_id=? AND currency_symbol=?",
                       (user_id, currency_symbol))
        con.commit()
        return True
    except Exception as e:
        return e


def set_favorite_pairs(user_id, favorite_pairs, con):
    cursor = con.cursor()
    cursor.execute("UPDATE users SET favorite_pairs=? WHERE user_id=?", (favorite_pairs, user_id))
    con.commit()
