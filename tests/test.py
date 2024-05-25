import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from aiogram import types

from handlers.callback_handler import to_back
from utils import get_main_menu_keyboard
from services.binance_api import get_account_info, get_info_currency
from services.get_top_list import main
from services.service_forever_currency import (
    get_forever_list,
    send_request_for_add_new_pair,
    send_request_for_delete_pair,
)


@pytest.fixture
def mock_get_connection():
    with patch("services.service_forever_currency.get_connection") as mock_conn:
        yield mock_conn


@pytest.fixture
def mock_get_favorite_pairs(mock_get_connection):
    with patch("services.service_forever_currency.get_favorite_pairs") as mock_get_pairs:
        yield mock_get_pairs


@pytest.fixture
def mock_add_new_favorite_pair(mock_get_connection):
    with patch("services.service_forever_currency.add_new_favorite_pair") as mock_add_pair:
        yield mock_add_pair


@pytest.fixture
def mock_delete_favorite_pair(mock_get_connection):
    with patch("services.service_forever_currency.delete_favorite_pair") as mock_delete_pair:
        yield mock_delete_pair


def test_get_forever_list_no_pairs(mock_get_favorite_pairs):
    mock_get_favorite_pairs.return_value = None
    result = get_forever_list(123)
    assert result is None


def test_get_forever_list_with_pairs(mock_get_favorite_pairs):
    mock_get_favorite_pairs.return_value = ["BTCUSDT", "ETHUSDT"]
    result = get_forever_list(123)
    assert result == ["BTCUSDT", "ETHUSDT"]


def test_send_request_for_add_new_pair_success(mock_add_new_favorite_pair):
    mock_add_new_favorite_pair.return_value = True
    result = send_request_for_add_new_pair(123, "BNBUSDT")
    assert result is True


def test_send_request_for_add_new_pair_failure(mock_add_new_favorite_pair):
    mock_add_new_favorite_pair.return_value = False
    result = send_request_for_add_new_pair(123, "BNBUSDT")
    assert result is False


def test_send_request_for_delete_pair_success(mock_delete_favorite_pair):
    mock_delete_favorite_pair.return_value = True
    result = send_request_for_delete_pair(123, "BTCUSDT")
    assert result is True


def test_send_request_for_delete_pair_failure(mock_delete_favorite_pair):
    mock_delete_favorite_pair.return_value = False
    result = send_request_for_delete_pair(123, "BTCUSDT")
    assert result is False


class TestCallbackHandler:
    @pytest.mark.asyncio
    @patch('aiogram.types.CallbackQuery')
    async def test_to_back(self, mock_callback_query):
        mock_callback_query.from_user.first_name = "John"
        mock_callback_query.message.edit_text = AsyncMock()
        mock_callback_query.message.reply_markup = MagicMock()

        await to_back(mock_callback_query)

        expected_reply_markup = get_main_menu_keyboard()
        mock_callback_query.message.edit_text.assert_called_once_with(
            "Hi, John! You are in main menu: ",
            reply_markup=expected_reply_markup
        )


class TestBinanceApi:
    @patch('services.binance_api.get_client')
    async def test_get_account_info(self, mock_get_client):
        mock_get_client.return_value.get_account.return_value = "Account info"
        result = await get_account_info()
        assert result == "Account info"

    @patch('services.binance_api.AsyncClient.create')
    async def test_get_info_currency(self, mock_create):
        mock_create.return_value.get_exchange_info.return_value = {
            "symbols": [{"symbol": "BTCUSDT"}, {"symbol": "ETHUSDT"}]}
        mock_create.return_value.get_ticker.return_value = {"lastPrice": "29500.50"}
        result = await get_info_currency("BTC")
        assert result == ({"symbol": "BTCUSDT"}, "29500.50")


class TestBinanceTop50:
    @patch('requests.get')
    def test_main_success(self, mock_get):
        mock_data = [
            {"symbol": "BTCUSDT", "askPrice": "29500.50", "priceChangePercent": "0.35", "quoteVolume": "200000000"},
            {"symbol": "ETHUSDT", "askPrice": "1850.25", "priceChangePercent": "-1.20", "quoteVolume": "150000000"},
            {"symbol": "BNBUSDT", "askPrice": "240.15", "priceChangePercent": "0.85", "quoteVolume": "100000000"},
        ]
        mock_get.return_value.json.return_value = mock_data

        result = main()

        expected_output = (
            "1. BTCUSDT - Price: 29500.50 USDT, Change in 24h: 0.35%\n"
            "2. ETHUSDT - Price: 1850.25 USDT, Change in 24h: -1.20%\n"
            "3. BNBUSDT - Price: 240.15 USDT, Change in 24h: 0.85%"
        )
        assert result.strip() == expected_output
