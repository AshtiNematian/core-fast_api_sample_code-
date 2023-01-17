import requests


class MarketList:

    def fetch(self):
        url = "https://api.coinex.com/v1/market/list"
        try:
            ss = requests.get(url)
            return ss.json()
        except Exception as e:
            print(str(e))
            print("Connection refused")

