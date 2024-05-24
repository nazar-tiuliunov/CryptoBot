from db.base import get_connection, get_favorite_pairs, add_new_favorite_pair, delete_favorite_pair


def get_forever_list(user_id):
    pairs = get_favorite_pairs(user_id, con=get_connection())
    if pairs is None:
        return None
    return pairs


def send_request_for_add_new_pair(user_id, currency_symbol):
    result = add_new_favorite_pair(user_id, currency_symbol, con=get_connection())
    return result


def send_request_for_delete_pair(user_id, currency_symbol):
    result = delete_favorite_pair(user_id, currency_symbol, con=get_connection())
    return result
