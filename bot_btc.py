import pprint
import websocket
import json
from binance.client import Client
from binance.enums import *
import config as config

symbol = 'BTCUSDT'
SOCKET = "wss://stream.binance.com:9443/ws/" + symbol.lower() + "@kline_1m"
client = Client(config.API_KEY, config.API_SECRET)

wallet = 100
per_order = 2
profit_pc = 0.01
profit_ratio = (1 + profit_pc / 100)
target_price = 0


# This is the code for placing first order
# order = client.create_test_order(
#     symbol='BTCUSDT',
#     side=Client.SIDE_BUY,
#     type=Client.ORDER_TYPE_MARKET,
#     quantity=0.001)

# res = client.get_orderbook_ticker(symbol='BTCUSDT')
# print(res)
# print(client.get_symbol_ticker(symbol='BTCUSDT')['price'])

def buy_crypto():
    global wallet, target_price
    buy_price = float(client.get_symbol_ticker(symbol=symbol)['price'])
    target_price = profit_ratio * buy_price
    print("Buying price is " + str(buy_price))
    print("Target price is " + str(target_price))
    print("Difference in dollars is " + str(target_price - buy_price))
    wallet = wallet - per_order
    print("Bought crypto... current wallet balance is $" + str(wallet))


def sell_crypto():
    global wallet
    wallet = wallet + per_order * profit_ratio
    print("Sold crypto... current wallet balance is $" + str(wallet))
    print("Yay! we got a profit of " + str(profit_pc) + "%")
    buy_crypto()


def on_open(w_s):
    print("Socket connected!")


def on_close(w_s):
    print("Socket disconnected!")


def on_message(w_s, message):
    global wallet
    json_message = json.loads(message)
    close_price = float(json_message['k']['c'])
    # print(close_price)
    if close_price >= target_price:
        sell_crypto()


def start_process(sym):
    global symbol
    symbol = sym
    buy_crypto()
    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
    ws.run_forever()


start_process(sym='BTCUSDT')
