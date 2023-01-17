import pandas as pd
import requests


class FetchKLineData:
    def __init__(self, symbol, type, limit=1000):
        self.symbol = symbol
        self.type = type
        self.limit = limit

    def fetch(self):
        url = f"https://api.coinex.com/v1/market/kline?market={self.symbol}&type={self.type}&limit={self.limit}"
        try:
            ss = requests.get(url)
            return ss.json()
        except Exception as e:
            print(str(e))
            print("Connection refused")

    def get(self):
        crypto = self.fetch()
        crypto_df = pd.DataFrame(crypto['data'],
                                 columns=['Time_', 'Open', 'Close', 'High', 'Low', 'Volume', 'Amount'])
        crypto_df['Close'] = pd.to_numeric(crypto_df['Close'], downcast='integer')
        crypto_df['date'] = pd.to_datetime(crypto_df['Time_'], unit='s')
        crypto_df = crypto_df.set_index('date')
        return crypto_df
