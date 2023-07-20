import requests
import os
from collections import namedtuple

DEFAULT_DOMAIN = "https://pro-api.coinmarketcap.com"
API_KEY = "91a039ac-1eae-4591-8892-5e5493148b8e"
EURO_ID = 2790
USD_ID = 2781
CRYPTOCURRENCY_LIMIT = 1000
CRYPTOCURRENCY = namedtuple("Cryptocurrency", ["name", "symbol", "coin_market_cap_id", "price", "market_cap_by_cmc",
                                               "percent_change_24h", "percent_change_7d", "circulating_supply",
                                               "total_supply", "infinite_supply", "market_cap", "market_cap_dominance"])


def crypto_prices_list(currency="EUR", display_limit=25):

    try:
        display_limit = int(display_limit)
    except TypeError:
        print("Invalid display limit, display limit should be integer")
        return True

    if currency == "USD":
        currency = USD_ID
        fiat_symbol = "$"
    elif currency == "EUR":
        currency = EURO_ID
        fiat_symbol = "€"
    else:
        print("Invalid currency name, try again")
        return True

    latest_data = requests.get(DEFAULT_DOMAIN + "/v1/cryptocurrency/listings/latest",
                               params={"CMC_PRO_API_KEY": API_KEY, "limit": CRYPTOCURRENCY_LIMIT,
                                       "convert_id": currency})
    cryptocurrencies = map(lambda x: crypto_call_to_namedtuple(x, currency), latest_data.json()["data"])

    # Displaying price of cryptocurrency by user choice
    print("Rank".ljust(5), "Name".ljust(20), "Symbol".ljust(7), "Price".ljust(11), "% 24H".ljust(7), "% 7D")
    for i, coin in enumerate(cryptocurrencies):
        if i < display_limit:
            print(str(i + 1).ljust(5), str(coin.name)[:20].ljust(20), str(coin.symbol).ljust(7),
                  f"{round(coin.price, 2)} {fiat_symbol}".ljust(11), f"{str(round(coin.percent_change_24h, 2))}%".ljust(7),
                  f"{str(round(coin.percent_change_7d, 2))}%")
        else:
            break


def crypto_call_to_namedtuple(call, currency=EURO_ID):
    name = call["name"]
    symbol = call["symbol"]
    crypto_id = call["id"]
    price = call["quote"][f"{currency}"]["price"]
    market_cap_cmc = call["cmc_rank"]
    percent_change_24h = call["quote"][f"{currency}"]["percent_change_24h"]
    percent_change_7d = call["quote"][f"{currency}"]["percent_change_7d"]
    circulating_supply = call["circulating_supply"]
    total_supply = call["total_supply"]
    infinite_supply = call["infinite_supply"]
    market_cap = call["quote"][f"{currency}"]["market_cap"]
    market_cap_dominance = call["quote"][f"{currency}"]["market_cap_dominance"]

    return CRYPTOCURRENCY(name, symbol, crypto_id, price, market_cap_cmc, percent_change_24h,
                          percent_change_7d, circulating_supply, total_supply, infinite_supply,
                          market_cap, market_cap_dominance)


def actions(user_input):

    def help():
        print("Command".ljust(14), "Info")
        print("info-(symbol)".ljust(14), "output addtional information about cryptocurrencies (optional parameter -(fiat) default euros")
        print("display".ljust(14), "output list of cryptocurrencies (optional parameter -(display limit) max 1000) default fiat currency in euros")
        print("displayeur".ljust(14), "outputs list of cryptocurrencies in euros (optional parameter -(display limit) max 1000)")
        print("displayusd".ljust(14), "outputs list of cryptocurrencies in dollars (optional parameter -(display limit) max 1000)")
        print("end".ljust(14), "immediately ends the program")

    def coin_info(currency_parameter="EUR", coin_symbol="BTC"):

        if currency_parameter == "USD":
            currency = USD_ID
            currency_sign = "$"
        elif currency_parameter == "EUR":
            currency = EURO_ID
            currency_sign = "€"
        else:
            print("Invalid currency name, try again")
            return True

        latest_data = requests.get(DEFAULT_DOMAIN + "/v1/cryptocurrency/listings/latest",
                                   params={"CMC_PRO_API_KEY": API_KEY, "limit": CRYPTOCURRENCY_LIMIT,
                                           "convert_id": currency})
        cryptocurrencies = map(lambda x: crypto_call_to_namedtuple(x, currency), latest_data.json()["data"])
        symbols = map(lambda x: x["symbol"], latest_data.json()["data"])

        if coin_symbol not in list(symbols):
            print("Invalid symbol, try again")
        else:
            for coin in cryptocurrencies:
                if coin.symbol == coin_symbol:
                    left_just = 22
                    print("Name".ljust(left_just), coin.name)
                    print("Symbol".ljust(left_just), coin.symbol)
                    print("Rank".ljust(left_just), coin.coin_market_cap_id)
                    print("Price".ljust(left_just), f"{round(coin.price, 2):,}{currency_sign}")
                    print("% 24H".ljust(left_just), f"{round(coin.percent_change_24h, 2)}%")
                    print("% 7D".ljust(left_just), f"{round(coin.percent_change_7d, 2)}%")
                    print("Circulating-Supply".ljust(left_just), f"{round(coin.circulating_supply):,}")
                    print("Total-Supply".ljust(left_just), f"{round(coin.total_supply):,}")
                    print("Infinite-Supply".ljust(left_just), coin.infinite_supply)
                    print("Market-Cap".ljust(left_just), f"{round(coin.market_cap, 2):,}{currency_sign}")
                    print("Market-Cap-Dominance".ljust(left_just), f"{round(coin.market_cap_dominance, 2)}%")
                    break

        return True

    # Distinquish between actions and actions with parameter
    user_input = user_input.split("-")
    parameter = ""
    second_parameter = ""
    if len(user_input) == 1:
        action = user_input[0]
    elif len(user_input) == 2:
        action, parameter = user_input
    elif len(user_input) == 3:
        action, parameter, second_parameter = user_input

    # Types of options via commands
    if action == "help":
        help()
    elif action == "end":
        return True
    elif action == "display":
        if parameter:
            if second_parameter:
                crypto_prices_list(currency=second_parameter.upper(), display_limit=parameter)
            else:
                crypto_prices_list(display_limit=parameter)
        else:
            crypto_prices_list()
    elif action == "info" and parameter:
        if second_parameter:
            coin_info(second_parameter.upper(), parameter.upper())
        else:
            coin_info(coin_symbol=parameter.upper())
    else:
        print("Wrong choice, try again")
        print("For list of commands type: help")


def main():
    crypto_prices_list()
    while True:

        print()
        user_input = input("Input: ")
        os.system("cls")
        program_state = actions(user_input)

        if program_state:
            break


if __name__ == "__main__":
    main()
