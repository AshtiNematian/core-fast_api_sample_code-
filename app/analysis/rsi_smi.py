from ta.momentum import RSIIndicator


import pandas as pd
from ta.trend import SMAIndicator


class RSISMI:
    def __init__(self, price_history):
        self.price_history = price_history

    def prepare_price_history(self):
        rsi = RSIIndicator(close=self.price_history['Close'], window=28)
        self.price_history['rsi'] = rsi.rsi()
        rsi_smi = SMAIndicator(close=rsi.rsi(), window=14)
        self.price_history['rsi_sma'] = rsi_smi.sma_indicator()

    def calculate_actions(self, time_period=14):
        rsi = self.price_history['rsi']
        rsi_sma = self.price_history['rsi_sma']
        action_df = pd.DataFrame(
            columns=['close',
                     'action',
                     'value',
                     'date'])
        for i in range(len(rsi)):
            try:
                if rsi[i] > rsi_sma[i] and rsi[i - 1] < rsi_sma[i - 1]:
                    close = self.price_history.loc[self.price_history.index[i], 'Close']
                    date = self.price_history.index[i]
                    action = 'buy'
                    value = rsi[self.price_history.index[i]]
                    sr = pd.Series([close, action, value, date], index=action_df.columns)
                    action_df = action_df.append(sr, ignore_index=True)

                elif rsi[i] < rsi_sma[i] and rsi[i - 1] > rsi_sma[i - 1]:
                    close = self.price_history.loc[self.price_history.index[i], 'Close']
                    date = self.price_history.index[i]
                    action = 'sell'
                    value = rsi[self.price_history.index[i]]
                    sr = pd.Series([close, action, value, date], index=action_df.columns)
                    action_df = action_df.append(sr, ignore_index=True)

            except Exception as e:
                print(f"error in macd_actions_calculator {e}")
        return action_df


    @staticmethod
    def calculate_backtest(action_df):
        pct_change_list = []
        row_counter = 0
        while row_counter < len(action_df):
            action = action_df['action'].iloc[row_counter]
            if action == 'sell' and row_counter < len(action_df) - 1:
                start = action_df['close'].iloc[row_counter]
                end = action_df['close'].iloc[row_counter + 1]
                pct_change = (start - end) / start
                pct_change = abs(pct_change) * 100
                pct_change_list.append(pct_change)
            if action == 'buy' and row_counter < len(action_df) - 1:
                start = action_df['close'].iloc[row_counter]
                end = action_df['close'].iloc[row_counter + 1]
                pct_change = (start - end) / start
                pct_change = abs(pct_change) * 100
                pct_change_list.append(pct_change)
            row_counter += 1

        return sum(pct_change_list)

    def calculate(self):
        self.prepare_price_history()
        action_df = self.calculate_actions()
        action_df['date'] = action_df['date'].astype(str)
        del action_df['value']
        back_test = self.calculate_backtest(action_df=action_df)
        return {
            "action_df": (action_df).to_dict(orient='records'),
            "back_test": back_test
        }


if __name__ == '__main__':
    from app.coinex.fetch_kline_data import FetchKLineData

    data = FetchKLineData(symbol="btcusdt", type="1day", limit=1000).get()
    rsi = RSISMI(data)
    print(rsi.calculate())
