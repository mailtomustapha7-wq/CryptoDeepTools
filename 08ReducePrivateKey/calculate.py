import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from shared_utils.crypto_math import h, modinv, SECP256K1_ORDER

N = SECP256K1_ORDER

A = 0x00000000000000000000000000000000000000000000000000000000795f9c63
B = 0xdac19ec586ea8aa454fd2e7090e3244cdf75a73bdb1aa970d8b0878e75df3cae


print(h(((A) * modinv(B, N)) % N))
