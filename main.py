import requests
import json

DEFAULT_DOMAIN = "https://pro-api.coinmarketcap.com"
API_KEY = "91a039ac-1eae-4591-8892-5e5493148b8e"
EURO_ID = 2790

r = requests.get(DEFAULT_DOMAIN + "/v1/cryptocurrency/listings/latest", params={"CMC_PRO_API_KEY": API_KEY, "limit": 1, "convert_id": EURO_ID})

#formatted_data = json.dumps(r.json(), indent=2)
#print(formatted_data)

bitcoin_data_json = r.json()
print("Time: " + str(bitcoin_data_json["status"]["timestamp"]))
print("Bitcoin price is " + str(bitcoin_data_json["data"][0]["quote"][f"{EURO_ID}"]["price"]) + " Euro")

