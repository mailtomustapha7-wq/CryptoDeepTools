import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from shared_utils.crypto_math import h, modinv, SECP256K1_ORDER

N = SECP256K1_ORDER

K = 0x6251240a6cb656310dbd7f0da53a315ab88ec253352a5d5481ee08e977b6ef2d
R = 0x331353fedfd6e4d6805fc1f06443ade552a43a43237fb6c3de3c7f0969b4cc67
S = 0x0bfec7e7d2ae249b3d69cd8d666b5ee833394af3b0703fa023579200d9ab2ff4
Z = 0x9d86bea51385f6a56835d0148e7f23a353605bab339127e800112307e6727d2d


print(h((((S * K) - Z) * modinv(R, N)) % N))
