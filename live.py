import requests

from crypto import convert_num, to_little
from mine import try_mining

url = "https://btc.getblock.io/mainnet/"

Headers = {"x-api-key": "68e450ba-28f9-4c8b-a8b1-ec8695c2abbd"}
data = {
    "jsonrpc": "2.0",
    "id": "getblock.io",
    "method": "getblocktemplate",
    "params": [
        {
            "rules": [
                "segwit"
            ]
        }
    ]
}

response = requests.post(url, json=data, headers=Headers)

print("Status Code", response.status_code)
data = response.json()['result']

version = data['version']
prev_hash = data['previousblockhash']
merkle_root = '54e1e701a075a315e6de9b298577a4fbfc837043b2b1b091319265f46c94808f'  # To be calculated
epoch = data['curtime']  # This is being set by us, although we're receiving it from the API
bits = int(data['bits'], 16)
next_height = data['height']
target_hex = data['target']

header_hex = convert_num(version) + to_little(prev_hash) + to_little(merkle_root) + convert_num(epoch) + convert_num(
    bits)
try_mining(header_hex, bits)
