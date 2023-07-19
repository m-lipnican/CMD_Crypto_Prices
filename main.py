import requests
import os
from collections import namedtuple

DEFAULT_DOMAIN = "https://pro-api.coinmarketcap.com"
API_KEY = "91a039ac-1eae-4591-8892-5e5493148b8e"
EURO_ID = 2790
USD_ID = 2781
CRYPTOCURRENCY = namedtuple("Cryptocurrency", ["name", "symbol", "coin_market_cap_id", "price", "market_cap_by_cmc", "percent_change_24h", "percent_change_7d"])
CRYPTOCURRENCY_LIMIT = 20


def crypto_prices_list(currency=EURO_ID):

    if currency == USD_ID:
        fiat_symbol = "$"
    elif currency == EURO_ID:
        fiat_symbol = "€"

    latest_data = requests.get(DEFAULT_DOMAIN + "/v1/cryptocurrency/listings/latest",
                               params={"CMC_PRO_API_KEY": API_KEY, "limit": CRYPTOCURRENCY_LIMIT,
                                       "convert_id": currency})
    price_of_cryptocurrencies = map(lambda x: crypto_call_to_namedtuple(x, currency), latest_data.json()["data"])

    # Displaying price of cryptocurrency by user choice
    print("Rank".ljust(5), "Name".ljust(15), "Symbol".ljust(7), "Price".ljust(11), "% 24H".ljust(7), "% 7D")
    for i, coin in enumerate(price_of_cryptocurrencies):
        print(str(i + 1).ljust(5), str(coin.name).ljust(15), str(coin.symbol).ljust(7),
              f"{round(coin.price, 2)} {fiat_symbol}".ljust(11), f"{str(round(coin.percent_change_24h, 2))}%".ljust(7),
              f"{str(round(coin.percent_change_7d, 2))}%")


def crypto_call_to_namedtuple(call, currency=EURO_ID):
    name = call["name"]
    symbol = call["symbol"]
    crypto_id = call["id"]
    price = call["quote"][f"{currency}"]["price"]
    market_cap = call["cmc_rank"]
    percent_change_24h = call["quote"][f"{currency}"]["percent_change_24h"]
    percent_change_7d = call["quote"][f"{currency}"]["percent_change_7d"]
    return CRYPTOCURRENCY(name, symbol, crypto_id, price, market_cap, percent_change_24h, percent_change_7d)


def actions(user_input):

    def help():
        print("List of action commands")
        print("info-(symbol/name) output addtional information about cryptocurrencies")
        print("display output list of cryptocurrencies (default is euros)")
        print("displayeur outputs list of cryptocurrencies in Euros")
        print("displayusd outputs list of cryptocurrencies in Dollars")

    def displaycoin():
        pass

    if user_input == "help":
        help()
    elif user_input == "end":
        return True
    elif user_input == "displayeur" or user_input == "display":
        crypto_prices_list()
    elif user_input == "displayusd":
        crypto_prices_list(USD_ID)
    elif "displaycoin" in user_input:
        displaycoin()


def main():
    crypto_prices_list()
    while True:

        user_input = input("Input (action)-(symbol/name): ")
        os.system("cls")
        program_state = actions(user_input)

        if program_state:
            break


if __name__ == "__main__":
    main()
