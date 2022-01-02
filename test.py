from datetime import datetime
from main import buy_sell_logic
import pandas as pd
import numpy as np

# # curs = ['ETH', 'BTC', 'BNB', 'SOL', 'XRP']
# curs = ['XRPUSDT', 'MATICUSDT', 'DOGEUSDT', 'SHIBUSDT']
#
# fromDate = str(datetime.strptime('01/09/2021', '%d/%m/%Y'))
# toDate = str(datetime.strptime('01/12/2021', '%d/%m/%Y'))
#
# total_amount = 100
# amount_per_cur = total_amount / len(curs)
#
# for cur in curs:
#     total_amount += buy_sell_logic(cur, amount_per_cur, fromDate, toDate)
#
# # print('Final amount after 30 days ' + str(total_amount))
# buy_sell_logic(curs[2], amount_per_cur, fromDate, toDate)

# Try to find out how long it took on average to get 1% increase in price
# Maybe I need to open position in a different time or based on different logic
# There's also short position
from mine import try_mining

df = pd.read_csv('test_data.csv')

row = df.iloc[11]
# print('Trying to mine... ' + str(index))
try_mining(row['header'], row['bits'])
print('Actual nonce is ' + str(row['nonce']))
print('\n')

# arr = df['nonce_hex'].apply(lambda x: int(x, 16)).to_numpy()
# arr = arr[:5000]
# perc = (arr > 1000000000).sum() * 100 / np.size(arr)
# print('Around this much percentage of times nonce is greater than 1 billion: ' + str(perc))
# So the figure is turning out to be around 70%
