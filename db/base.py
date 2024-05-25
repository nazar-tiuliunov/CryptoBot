"""
Module containing functions for interacting with the SQLite database.
"""

import sqlite3
import os


def get_connection():
    """
        Establishes a connection to the SQLite database.

        Returns:
            sqlite3.Connection: Connection object representing the database connection.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    database = os.path.join(base_dir, 'database.db')
    return sqlite3.connect(database)


def create_table(con):
    """
        Creates necessary tables in the database if they don't exist.

        Args:
            con (sqlite3.Connection): Connection object representing the database connection.
    """
    cursor = con.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username VARCHAR(32),
                user_first_name VARCHAR(32),
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
    """
        Inserts a new user into the users table.

        Args:
            user_id (int): The ID of the user.
            username (str): The username of the user.
            user_first_name (str): The first name of the user.
            con (sqlite3.Connection): Connection object representing the database connection.
    """
    cursor = con.cursor()
    cursor.execute("INSERT INTO users (user_id, username, user_first_name) VALUES (?, ?, ?)",
                   (user_id, username, user_first_name))
    con.commit()


def get_user_by_id(user_id, con):
    """
        Retrieves a user from the users table by their ID.

        Args:
            user_id (int): The ID of the user.
            con (sqlite3.Connection): Connection object representing the database connection.

        Returns:
            tuple: A tuple representing the user's information if found, otherwise None.
    """
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()


def get_favorite_pairs(user_id, con):
    """
    Retrieves favorite currency pairs associated with a user from the database.

    Args:
        user_id (int): The ID of the user.
        con (sqlite3.Connection): Connection object representing the database connection.

    Returns:
        list: A list of tuples representing the favorite currency pairs, or None if no pairs found.
    """
    cursor = con.cursor()
    cursor.execute("SELECT currency_symbol FROM favorite_currencies WHERE user_id=?", (user_id,))
    result = cursor.fetchall()
    return result if result else None


def add_new_favorite_pair(user_id, currency_symbol, con):
    """
        Adds a new favorite currency pair for a user to the database.

        Args:
            user_id (int): The ID of the user.
            currency_symbol (str): The symbol of the currency pair to add.
            con (sqlite3.Connection): Connection object representing the database connection.

        Returns:
            bool or Exception: True if the pair was added successfully, otherwise an exception.
    """
    cursor = con.cursor()
    try:
        cursor.execute("INSERT INTO favorite_currencies (user_id, currency_symbol) VALUES (?, ?)",
                       (user_id, currency_symbol))
        con.commit()
        return True
    except Exception as e:
        return e


def delete_favorite_pair(user_id, currency_symbol, con):
    """
        Deletes a favorite currency pair for a user from the database.

        Args:
            user_id (int): The ID of the user.
            currency_symbol (str): The symbol of the currency pair to delete.
            con (sqlite3.Connection): Connection object representing the database connection.

        Returns:
            bool or Exception: True if the pair was deleted successfully, otherwise an exception.
    """
    cursor = con.cursor()
    try:
        cursor.execute("DELETE FROM favorite_currencies WHERE user_id=? AND currency_symbol=?",
                       (user_id, currency_symbol))
        con.commit()
        return True
    except Exception as e:
        return e


def set_favorite_pairs(user_id, favorite_pairs, con):
    """
        Updates the favorite currency pairs for a user in the database.

        Args:
            user_id (int): The ID of the user.
            favorite_pairs (list): A list of tuples representing the favorite currency pairs.
            con (sqlite3.Connection): Connection object representing the database connection.
    """
    cursor = con.cursor()
    cursor.execute("UPDATE users SET favorite_pairs=? WHERE user_id=?", (favorite_pairs, user_id))
    con.commit()
