import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from shared_utils.crypto_math import h, modinv, SECP256K1_ORDER

N = SECP256K1_ORDER

K = 0x5d4bc1aa9668f2286151499508869fd31e07f4a9e7dd09f5f6dc4634464dd58d
R = 0x15e3f8b110a2baf09ddcce139644888bda303cd4d0a37c872e5faceb57abff01
S = 0x2d2ca770322bfad7a32ae2568869512f71b8c40a561a7109a54f2799953342e3
Z = 0x793c00bdb7c96e19cb2670f3aec5369558b64f0e12645af070d94c2fc06db6ed


print(h((((S * K) - Z) * modinv(R, N)) % N))
