import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from shared_utils.crypto_math import h, modinv, SECP256K1_ORDER

N = SECP256K1_ORDER

K = 0x39588951cd20e38a6dc86d6b436da7abd2bcad84af3dd16b6f8a83c946c1d3c6
R = 0xaafe80d17b0d30de09cbe39a85514aaae0a388135987ab80207e1eed3c915280
S = 0x0d46fb28a4b30599d33325aa8b7633dd0f584f8125bb2e136c88a3e91a6f4238
Z = 0xbbfd05c3355957cbdf44d283b9199eb9741f775a16081288187a82f544fac11f


print(h((((S * K) - Z) * modinv(R, N)) % N))
