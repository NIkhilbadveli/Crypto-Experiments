import time
from binascii import unhexlify, hexlify

import requests

from crypto import convert_num, to_little, int_to_hex_string
from mine import try_mining
from hashlib import sha256


# raw = '0100000001c997a5e56e104102fa209c6a852dd90660a20b2d9c352423edce25857fcd3704000000004847304402204e45e16932b8af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb8cd410220181522ec8eca07de4860a4acdd12909d831cc56cbbac4622082221a8768d1d0901ffffffff0200ca9a3b00000000434104ae1a62fe09c5f51b13905f07f06b99a2f7159b2225f374cd378d71302fa28414e7aab37397f554a7df5f142c21c1b7303b8a0626f1baded5c72a704f7e6cd84cac00286bee0000000043410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3ac00000000'

def tx_encode_coinbase_height(height):
    """
    Encode the coinbase height, as per BIP 34:
    https://github.com/bitcoin/bips/blob/master/bip-0034.mediawiki
    Arguments:
        height (int): height of the mined block
    Returns:
        string: encoded height as an ASCII hex string
    """

    width = (height.bit_length() + 7) // 8

    return bytes([width]).hex() + convert_num(height)


def bitcoinaddress2hash160(addr):
    """
    Convert a Base58 Bitcoin address to its Hash-160 ASCII hex string.
    Args:
        addr (string): Base58 Bitcoin address
    Returns:
        string: Hash-160 ASCII hex string
    """

    table = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    hash160 = 0
    addr = addr[::-1]
    for i, c in enumerate(addr):
        hash160 += (58 ** i) * table.find(c)

    # Convert number to 50-byte ASCII Hex string
    hash160 = "{:050x}".format(hash160)

    # Discard 1-byte network byte at beginning and 4-byte checksum at the end
    return hash160[2:50 - 8]


def build_transaction(coinbase_message, height, address):
    tx_version = '01000000'
    input_count = '01'
    input_tx_id = '0000000000000000000000000000000000000000000000000000000000000000'  # This is actually previous output tx_id if it's not a coinbase transaction
    input_index = 'ffffffff'

    # There's a format to calculate this. Any random message can be put here
    coinbase_script = tx_encode_coinbase_height(height) + hexlify(coinbase_message.encode()).decode()
    coinbase_script_size = int_to_hex_string(len(coinbase_script) // 2)

    sequence = 'ffffffff'
    tx_out_count = '01'
    amount_lx = convert_num(625000000)  # Amount in satoshis. 1 BTC = 100 million satoshis.

    # Another format for this. It holds my wallet address
    pub_script = "76" + "a9" + "14" + bitcoinaddress2hash160(address) + "88" + "ac"
    pub_script_size = int_to_hex_string(len(pub_script) // 2)
    lock_time = '00000000'

    return tx_version + input_count + input_tx_id + input_index + coinbase_script_size + coinbase_script + sequence + tx_out_count + amount_lx + pub_script_size + pub_script + lock_time


def get_merkle_root(tx_raw_data):
    # This is only for coinbase transaction
    calc_hash = sha256(sha256(unhexlify(tx_raw_data)).digest()).digest()
    tx_hash = hexlify(calc_hash[::-1]).decode("utf-8")  # In big-endian
    # It seems the transaction hash is being represented in big endian. I guess this will be the merkle root,
    # which I need to pass to my original function which will convert to little while packing together the header.
    print('Merkle root is... ' + tx_hash)
    return tx_hash


def build_block_to_submit():
    pass


def submit_block(block_hex):
    data = {
        "jsonrpc": "2.0",
        "id": "getblock.io",
        "method": "submitblock",
        "params": [
            block_hex,
            ""
        ]
    }

    response = requests.post(url, json=data, headers=Headers)

    print("Status Code", response.status_code)
    print(response.json())


# Example transaction with real data
# def build_transaction():
#     tx_version = '01000000'
#     input_count = '01'
#     input_tx_id = 'f3f6a909f8521adb57d898d2985834e632374e770fd9e2b98656f1bf1fdfd42701'  # This is actually previous output tx_id if it's not a coinbase transaction
#     input_index = '000000'
#     script_sig_size = '6b'
#     script_sig = '48304502203a776322ebf8eb8b58cc6ced4f2574f4c73aa664edce0b0022690f2f6f47c521022100b82353305988cb0ebd443089a173ceec93fe4dbfe98d74419ecc84a6a698e31d012103c5c1bc61f60ce3d6223a63cedbece03b12ef9f0068f2f3c4a7e7f06c523c3664'  # There's a format to calculate this. Any random message can be put here
#     sequence = 'ffffffff'
#     tx_out_count = '02'
#     amount_lx = '60e3160000000000'  # Amount in satoshis. 1 BTC = 100 million satoshis.
#     pub_script_size = '19'
#     pub_script = '76a914977ae6e32349b99b72196cb62b5ef37329ed81b488ac063d1000000000001976a914f76bc4190f3d8e2315e5c11c59cfc8be9df747e388ac'  # Another format for this. It holds my wallet address
#     lock_time = '00000000'
#
#     return tx_version + input_count + input_tx_id + input_index + script_sig_size + script_sig + sequence + tx_out_count + amount_lx + pub_script_size + pub_script + lock_time


my_wallet = '1HT3pdaFhKvDTipYvg6u8nUmyY4CA9cEuQ'

url = "https://btc.getblock.io/mainnet/"
Headers = {"x-api-key": "68e450ba-28f9-4c8b-a8b1-ec8695c2abbd", 'User-Agent': 'Mozilla/5.0'}


def get_block_template():
    post_data = {
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

    response = requests.post(url, json=post_data, headers=Headers)

    print("Status Code", response.status_code)
    return response.json()['result']


def mine_live():
    data = get_block_template()
    version = data['version']
    prev_hash = data['previousblockhash']
    next_height = data['height']
    tx_raw = build_transaction('I love you!', next_height, my_wallet)

    merkle_root = get_merkle_root(tx_raw)
    epoch = data['curtime']  # This is being set by us, although we're receiving it from the API
    bits = int(data['bits'], 16)

    target_hex = data['target']

    header_hex = convert_num(version) + to_little(prev_hash) + to_little(merkle_root) + convert_num(epoch) \
                 + convert_num(bits)
    print('Trying to mine the block... ' + str(next_height) + ' and time at ' + str(epoch))
    print('Raw transaction in hex \n' + tx_raw)
    found, initial_nonce, header_with_nonce = try_mining(header_hex, bits)
    if found:
        block_hex = header_with_nonce
        block_hex += int_to_hex_string(1)  # Number of transactions in the block
        block_hex += tx_raw
        print('Block in hex to be submitted \n' + block_hex)
        submit_block(block_hex)
    # else:
    #     print('Sleeping for 15 secs... so that other miners may mine')
    #     time.sleep(15)
    #     # Wait until new block is minted by others
    #     new_data = get_block_template()
    #     while new_data['previousblockhash'] == prev_hash:
    #         print('Sleeping for 5 secs...')
    #         time.sleep(5)
    #         new_data = get_block_template()
    #
    #     # Mine again with the new block as previous block hash
    #     mine_live(new_data)


# mine_live()
# for i in range(5):
#     get_block_template()
#     time.sleep(15)
