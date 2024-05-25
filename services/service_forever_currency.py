"""
Module containing functions for interacting with favorite currency pairs in the database.
"""
from db.base import get_connection, get_favorite_pairs, add_new_favorite_pair, delete_favorite_pair


def get_forever_list(user_id):
    """
        Retrieve the list of forever favorite currency pairs for a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list or None: A list of forever favorite currency pairs for the user,
            or None if no pairs are found.
    """
    pairs = get_favorite_pairs(user_id, con=get_connection())
    if pairs is None:
        return None
    return pairs


def send_request_for_add_new_pair(user_id, currency_symbol):
    """
        Send a request to add a new favorite currency pair for a user.

        Args:
            user_id (int): The ID of the user.
            currency_symbol (str): The symbol of the currency pair to add.

        Returns:
            bool: True if the pair was successfully added, False otherwise.
    """
    result = add_new_favorite_pair(user_id, currency_symbol, con=get_connection())
    return result


def send_request_for_delete_pair(user_id, currency_symbol):
    """
        Send a request to delete a favorite currency pair for a user.

        Args:
            user_id (int): The ID of the user.
            currency_symbol (str): The symbol of the currency pair to delete.

        Returns:
            bool: True if the pair was successfully deleted, False otherwise.
    """
    result = delete_favorite_pair(user_id, currency_symbol, con=get_connection())
    return result
