from binance.client import Client
from datetime import datetime
import pandas as pd
from config import API_KEY, API_SECRET


def get_historical_data(symbol, interval, fromDate, toDate):
    klines = client.get_historical_klines(symbol, interval, fromDate, toDate)
    df = pd.DataFrame(klines,
                      columns=['dateTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime', 'quoteAssetVolume',
                               'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])
    df.dateTime = pd.to_datetime(df.dateTime, unit='ms')
    df['date'] = df.dateTime.dt.strftime("%d/%m/%Y")
    df['time'] = df.dateTime.dt.strftime("%H:%M:%S")
    df = df.drop(['dateTime', 'closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol',
                  'ignore'], axis=1)
    column_names = ["date", "time", "open", "high", "low", "close", "volume"]
    df = df.reindex(columns=column_names)
    df['close'] = df['close'].astype('float64')
    df['high'] = df['high'].astype('float64')
    df['low'] = df['low'].astype('float64')
    return df


client = Client(API_KEY, API_SECRET)

fromDate = str(datetime.strptime('22/11/2021', '%d/%m/%Y'))
toDate = str(datetime.strptime('22/12/2021', '%d/%m/%Y'))
interval = Client.KLINE_INTERVAL_1MINUTE

upper_bound = round(1 + 1.5 / 100, 3)
lower_bound = round(1 - 5 / 100, 3)


def split_into_days(df):
    df = df[:-1]
    list_of_dfs = []
    start_time = df['date'][0]
    start = 0
    i = 0
    for index in df.index:
        if start_time != df['date'][index]:
            list_of_dfs.append(df.iloc[start: i])
            start_time = df['date'][index]
            start = i
        i += 1
    return list_of_dfs


def buy_sell_logic(symbol, amount, start_date, end_date):
    df_main = get_historical_data(symbol, interval, start_date, end_date)
    days_df = split_into_days(df_main)
    # epochs = get_epochs(datetime(2021, 12, 18, 5, 30), datetime(2021, 12, 23, 5, 30))
    total_profit = 0
    column_names = ['buy_time', 'buy_price', 'sell_time', 'sell_price', 'profit', 'total_profit']
    out_df = pd.DataFrame(columns=column_names)

    sold = False
    first_time = True
    for df in days_df:
        if sold or first_time:
            buy_price = df['close'].iloc[0]
            buy_time = df['date'].iloc[0] + ' ' + df['time'].iloc[0]
            sell_time = 0
            sell_price = 0
            profit = 0
            first_time = False

        for index, row in df.iterrows():
            sell_time = df['date'][index] + ' ' + df['time'][index]
            sell_price = row['close']
            if row['close'] >= buy_price * upper_bound:
                profit = amount * (sell_price - buy_price) / buy_price
                sold = True
                total_profit += profit
                out_row = [buy_time, buy_price, sell_time, sell_price, profit, total_profit]
                out_df = out_df.append(pd.Series(out_row, index=column_names), ignore_index=True)
                break
            elif sell_time.split(' ')[0] != buy_time.split(' ')[0] and row['close'] <= buy_price * lower_bound:
                profit = amount * (sell_price - buy_price) / buy_price
                total_profit += profit
                out_row = [buy_time, buy_price, sell_time, sell_price, profit, total_profit]
                out_df = out_df.append(pd.Series(out_row, index=column_names), ignore_index=True)
                sold = True
                break
            elif index == df.index[-1]:
                sold = False
                # profit = amount * (sell_price - buy_price) / buy_price

    print(out_df)
    print('Total profit after 30 days for ' + symbol + ' is :- ' + str(total_profit))
    return total_profit

# buy_sell_logic('ETHUSDT', 100, fromDate, toDate)
