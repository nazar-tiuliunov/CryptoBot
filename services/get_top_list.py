"""
Module containing a function to retrieve the top 50 cryptocurrencies from the Binance API.
"""
import requests


def main():
    """
        Retrieve the top 50 cryptocurrencies from the Binance API.

        Returns:
            str: A string containing information about the top 50 cryptocurrencies.
    """
    url = 'https://api.binance.com/api/v3/ticker/24hr'
    response = requests.get(url)
    data = response.json()

    usdt_pairs = [x for x in data if x['symbol'].endswith('USDT')]
    usdt_pairs = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
    usdt_pairs = [f"{i + 1}. {x['symbol']} - Price: {x['askPrice']} USDT, Change in 24h: {x['priceChangePercent']}%"
                  for i, x in enumerate(usdt_pairs)][:50]
    top_50 = '\n'.join(usdt_pairs)
    return top_50


if __name__ == '__main__':
    print(main())
