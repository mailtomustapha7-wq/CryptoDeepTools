import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from shared_utils.crypto_math import h, modinv, SECP256K1_ORDER

N = SECP256K1_ORDER

R = 0x83fe1c06236449b69a7bee5be422c067d02c4ce3f4fa3756bd92c632f971de06
S = 0x7405249d2aa9184b688f5307006fddc3bd4a7eb89294e3be3438636384d64ce7
Z = 0x070239c013e8f40c8c2a0e608ae15a6b1bb4b8fbcab3cff151a6e4e8e05e10b7
K = 0x070239C013E8F40C8C2A0E608AE15A6B23D4A09295BE678B21A5F1DCEAE1F634


print(h((((S * K) - Z) * modinv(R, N)) % N))
