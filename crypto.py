from binascii import unhexlify, hexlify
from hashlib import sha256
from timeit import default_timer as timer
from datetime import timedelta


def int_to_hex_string(num):
    # print(num)
    s = str(hex(num)[2:])
    return s if len(s) % 2 == 0 else '0' + s


def to_little(val):
    # print(val)
    little_hex = bytearray.fromhex(val)
    little_hex.reverse()
    # print("Byte array format:", little_hex)
    str_little = ''.join(format(x, '02x') for x in little_hex)
    return str_little


def convert_num(num):
    out_str = to_little(int_to_hex_string(num))
    # print(out_str)
    return out_str


def main():
    version = 1073676288
    prev_hash = '0000000000000000000bcbb69d6ebe4aa0825be5f48c2bfa62e4ca2f728b998a'
    merkle = '54e1e701a075a315e6de9b298577a4fbfc837043b2b1b091319265f46c94808f'
    timestamp = 1638349512
    bits = 386701843
    nonce = 64001806

    header_hex = convert_num(version) + to_little(prev_hash) + to_little(merkle) + convert_num(timestamp) + convert_num(
        bits) + convert_num(nonce)
    # header_hex = '0000ff3f8a998b722fcae462fa2b8cf4e55b82a04abe6e9db6cb0b0000000000000000008f80946cf465923191b0b1b2437083fcfba47785299bdee615a375a001e7e154c83aa761139a0c17' + convert_num(
    #     nonce)
    target_hex = int_to_hex_string(bits)
    target = int(target_hex[2:], 16) * 2 ** (8 * (int(target_hex[:2], 16) - 3))
    header_bin = unhexlify(header_hex)

    calc_hash = sha256(sha256(header_bin).digest()).digest()
    big_endian_hash = hexlify(calc_hash[::-1]).decode("utf-8")
    print(big_endian_hash)
    print(target)
    if int(big_endian_hash, 16) < target:
        print('Yayy! We found correct nonce.')


# main()
