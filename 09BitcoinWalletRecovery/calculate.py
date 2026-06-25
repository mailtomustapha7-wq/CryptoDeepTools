import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from shared_utils.crypto_math import h, modinv, SECP256K1_ORDER

N = SECP256K1_ORDER

K = 0x7fffffffffffffffffffffffffffffff5d576e7357a4501ddfe92f46681b20a0
R = 0x00000000000000000000003b78ce563f89a0ed9414f5aa28ad0d96d6795f9c63
S = 0x0a963d693c008f0f8016cfc7861c7f5d8c4e11e11725f8be747bb77d8755f1b8
Z = 0x521a65420faa5386d91b8afcfab68defa02283240b25aeee958b20b36ddcb6de


print(h((((S * K) - Z) * modinv(R, N)) % N))
