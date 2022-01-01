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
    version = 536870916
    prev_hash = '00000000000000000008924b9804c972fe8ed96a65f802e53366e78e3b1eb316'
    merkle = '85a5f3d34daeb8d7acb044a6b4c50451e0146de97bf2e24b735d6198e94800ea'
    timestamp = 1640219129
    bits = 386638367
    nonce = 4134816545

    header_hex = convert_num(version) + to_little(prev_hash) + to_little(merkle) + convert_num(timestamp) + convert_num(
        bits) + convert_num(nonce)

    target_hex = int_to_hex_string(bits)
    target = int(target_hex[2:], 16) * 2 ** (8 * (int(target_hex[:2], 16) - 3))
    header_bin = unhexlify(header_hex)

    calc_hash = sha256(sha256(header_bin).digest()).digest()
    big_endian_hash = hexlify(calc_hash[::-1]).decode("utf-8")
    print(big_endian_hash)
    print(target)
    if int(big_endian_hash, 16) < target:
        print('Yayy! We found correct nonce.')

