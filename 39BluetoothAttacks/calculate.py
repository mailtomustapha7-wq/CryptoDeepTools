import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from shared_utils.crypto_math import h, modinv, SECP256K1_ORDER

N = SECP256K1_ORDER

K = 0x6bd261bd25ac54807552dfeec6454d6719ec8a05cb11ad5171e1ad68abb0acb2
R = 0x5013dbed340fed00b6cb9778a713e1456b8138d00c3bcf6e7ff117be723335d0
S = 0x5018ddd352a6bc61b86afee5001a3e25d26a328a833c8f3812a15465f542c1c9
Z = 0x396ebf23dbcccce2a389ccb26198e25118bf7f72c38d2a4ab8d9e4648f2385f8


print(h((((S * K) - Z) * modinv(R, N)) % N))
