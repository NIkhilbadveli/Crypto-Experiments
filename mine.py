import itertools
from timeit import default_timer as timer
from datetime import timedelta

from tensorflow import keras
from keras.models import model_from_json

from crypto import convert_num, int_to_hex_string, to_little
from binascii import unhexlify, hexlify
from hashlib import sha256
import numpy as np


def load_model():
    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")
    loaded_model.compile(loss=keras.losses.BinaryCrossentropy(from_logits=True),
                         optimizer=keras.optimizers.SGD(learning_rate=0.5),
                         metrics=['accuracy'])
    return loaded_model


def check_hash_with_nonce(header, target, nonce_int):
    header_hex = header + convert_num(nonce_int)
    header_bin = unhexlify(header_hex)

    calc_hash = sha256(sha256(header_bin).digest()).digest()
    big_endian_hash = hexlify(calc_hash[::-1]).decode("utf-8")

    return big_endian_hash, int(big_endian_hash, 16) < target


def get_nonce(header):
    threshold = 0.03
    s = ''
    for hx in header:
        s += bin(int(hx, 16))[2:].zfill(4)
    x = np.fromiter((int(x) for x in list(s)), dtype=np.int32)
    y_raw = loaded_model.predict(x.reshape(1, 608))
    y_pred = np.where(y_raw > threshold, 1, 0)
    y_pred = y_pred[0]
    # should return 32 bit string of the nonce
    out_str = ''
    for bit in y_pred:
        out_str += str(bit)
    return out_str


def try_mining(header, bits):
    # r is number of wrong bits
    s = get_nonce(header)

    if len(s) != 32:
        print('Length of the binary sequence must be 32 bits!')
        print('current length is ' + str(len(s)))
        return
    initial_nonce = int(s, 2)
    print('Predicted nonce from the model:- ' + str(initial_nonce))
    r = [9, 8, 7, 6, 5]  # Until only 5 bits are wrong

    target_hex = int_to_hex_string(bits)
    target = int(target_hex[2:], 16) * 2 ** (8 * (int(target_hex[:2], 16) - 3))

    sum = 0
    for w_b in r:
        sum += find_comb(32, w_b)
    sum = int(sum)
    # print('Total possibilities:- ' + str(sum))

    found = False
    start = timer()
    j = 0
    for w_b in r:
        for tup in itertools.combinations(range(32), w_b):
            a = initial_nonce
            for i, pos in enumerate(tup):
                a = a ^ (1 << 31 - pos)
            calc_hash, less_than_target = check_hash_with_nonce(header, target, a)
            if less_than_target:
                # found = True
                print('Found nonce! Value is ' + str(a))
                print('Hash is ' + calc_hash)
                end = timer()
                print(timedelta(seconds=end - start))
                break

            j += 1
            if j == sum:  # all possible iterations
                print('Couldnt find nonce!')
                end = timer()
                print(timedelta(seconds=end - start))
                break
            # Can also check the mining logic here by sending this nonce to that function
            # Maybe we can improve this loop with binary search instead of going in sequence.
            # This is because the correct positions might be spread out randomly among the 32 positions
    return initial_nonce


def test_mine():
    version = 536870916
    prev_hash = '00000000000000000008924b9804c972fe8ed96a65f802e53366e78e3b1eb316'
    merkle = '85a5f3d34daeb8d7acb044a6b4c50451e0146de97bf2e24b735d6198e94800ea'
    timestamp = 1640219129
    bits = 386638367
    nonce = 4134816545

    header = convert_num(version) + to_little(prev_hash) + to_little(merkle) + convert_num(timestamp) + convert_num(
        bits)

    try_mining(header, bits)


def fact(k):
    f = i = 1
    while i <= k:
        f = i * f
        i += 1
    return f


def find_comb(x, y):
    num = fact(x)
    den = fact(x - y)
    den = fact(y) * den
    comb = num / den
    return comb


loaded_model = load_model()
# test_mine()
