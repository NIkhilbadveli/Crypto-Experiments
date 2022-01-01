import pandas as pd
import os
from crypto import convert_num, to_little
from calendar import timegm
import time
import numpy as np

# column_names = ['block_height', 'header_hash', 'nonce_hex']
# out_df = pd.DataFrame(columns=column_names)

# for filename in os.listdir('BlockData'):
#     df = pd.read_csv('BlockData' + '/' + filename, sep='\t')
#     print('Appending from... ' + filename)
#     for index, row in df.iterrows():
#         utc_time = time.strptime(row['time'], "%Y-%m-%d %H:%M:%S")
#         epoch_time = timegm(utc_time)
#         header_hash = convert_num(row['version']) + to_little(df.iloc[index - 1]['hash']) + to_little(
#             row['merkle_root']) + convert_num(epoch_time) + convert_num(row['bits'])
#         nonce_hex = convert_num(row['nonce'])
#         out_df = out_df.append(pd.Series([row['id'], header_hash, nonce_hex], index=column_names),
#                                ignore_index=True)
#
# out_df = out_df[1:]
# out_df.to_csv('output_data.csv')

# Nonce values are really large and very diverse (approx. 70% of the times in billions)
# column_names = ['block_height', 'nonce']
# out_df = pd.DataFrame(columns=column_names)
# nonces = []
# block_heights = []
# for filename in os.listdir('BlockData'):
#     df = pd.read_csv('BlockData' + '/' + filename, sep='\t')
#     print('Appending from... ' + filename)
#     list1 = df['nonce'].to_list()
#     nonces.extend([num for num in list1 if num < 1000000000])
#     block_heights.extend(df['id'].to_list())
#
# for x, y in zip(block_heights, nonces):
#     out_df = out_df.append(pd.Series([x, y], index=column_names), ignore_index=True)
#
# out_df.to_csv('nonce_data.csv')

column_names = ['x', 'y']
out_df = pd.DataFrame(columns=column_names)

for filename in os.listdir('BlockData'):
    df = pd.read_csv('BlockData' + '/' + filename, sep='\t')
    print('Appending from... ' + filename)
    for index, row in df.iterrows():
        utc_time = time.strptime(row['time'], "%Y-%m-%d %H:%M:%S")
        epoch_time = timegm(utc_time)
        header_hash = convert_num(row['version']) + to_little(df.iloc[index - 1]['hash']) + to_little(
            row['merkle_root']) + convert_num(epoch_time) + convert_num(row['bits'])
        s = ''
        for hx in header_hash:
            s += bin(int(hx, 16))[2:].zfill(4)
        x = np.fromiter((int(x) for x in list(s)), dtype=np.int32)
        nonce_hex = convert_num(row['nonce'])
        s = ''
        for hx in nonce_hex:
            s += bin(int(hx, 16))[2:].zfill(4)
        y = np.fromiter((int(x) for x in list(s)), dtype=np.int32)
        if len(nonce_hex) == 8 and len(header_hash) == 152:
            out_df = out_df.append(pd.Series([x, y], index=column_names),
                                   ignore_index=True)
out_df = out_df[1:]
out_df.to_csv('input_data.csv')
