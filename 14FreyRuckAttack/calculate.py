import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from shared_utils.crypto_math import h, modinv, SECP256K1_ORDER

N = SECP256K1_ORDER

K = 0xf99718ec8df44d695daa9eedd2b3cbe29d8a14a3fc026baeb279afe47c709de3
R = 0x061e5f5c2bc146cd5070cdef9cd2376a0b2fbbdbbda698858a38190d06caf1ff
S = 0x649db1b4fbaaba2d0669f7f7635157b273146b064248d04e76c25d41971d99a1
Z = 0xb8e936d143c8733bb1ede19146f8725fee1d10bfc19e14452a51cef0cb0014d8


print(h((((S * K) - Z) * modinv(R, N)) % N))
