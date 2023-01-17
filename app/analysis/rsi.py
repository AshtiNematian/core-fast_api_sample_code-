from ta.momentum import RSIIndicator

import pandas as pd


class RSI:
    def __init__(self, price_history):
        self.price_history = price_history

    def prepare_price_history(self):
        rsi = RSIIndicator(close=self.price_history['Close'])
        self.price_history['rsi'] = rsi.rsi()

    def calculate_actions(self, time_period=14):
        rsi = self.price_history['rsi']
        action_df = pd.DataFrame(
            columns=['close',
                     'action',
                     'value',
                     'date'])
        for i in range(len(rsi)-1):
            if rsi[rsi.index[i]] >= 50 and rsi[rsi.index[i + 1]] <= 50:
                close = self.price_history.loc[rsi.index[i + 1], 'Close']
                date = rsi.index[i + 1]
                action = "sell"
                value = rsi[rsi.index[i + 1]]
                sr = pd.Series([close, action, value, date], index=action_df.columns)
                action_df = action_df.append(sr, ignore_index=True)

            elif rsi[rsi.index[i]] <= 50 and rsi[rsi.index[i + 1]] >= 50:
                close = self.price_history.loc[rsi.index[i + 1], 'Close']
                date = rsi.index[i + 1]
                action = "buy"
                value = rsi[rsi.index[i + 1]]
                sr = pd.Series([close, action, value, date], index=action_df.columns)
                action_df = action_df.append(sr, ignore_index=True)
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

    data = FetchKLineData(symbol="adausdt", type="1hour", limit=100).get()
    rsi = RSI(data)
    print(rsi.calculate())
