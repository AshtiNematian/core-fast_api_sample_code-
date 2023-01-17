import ta
from app.coinex.fetch_kline_data import FetchKLineData
from ta.volatility import average_true_range


class ATR:
    def __init__(self, price_history):
        self.price_history = price_history

    def calculate(self):
        self.price_history['Atr'] = ta.volatility.AverageTrueRange(
            self.price_history.High.astype(float),
            self.price_history.Low.astype(float),
            self.price_history.Close.astype(float),
            window=14,
            fillna=False
        ).average_true_range()  # <- call function
        atr = self.price_history.Atr.iloc[-1]
        return {"atr": atr}


if __name__ == '__main__':
    from app.coinex.fetch_kline_data import FetchKLineData

    data = FetchKLineData(symbol="btcusdt", type="3min", limit=1000).get()
    atr = ATR(data)
    print(atr.calculate())
