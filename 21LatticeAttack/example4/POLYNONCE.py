import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from shared_utils.crypto_math import SECP256K1_ORDER
from shared_utils.polynonce import format_hex_key, load_signatures, compute_polynonce

with open("SignatureRSZ.csv") as myfile:
    listfile = "\n".join(f'{line.rstrip()[+5:-5]}' for line in myfile)

f = open("NoncesHEX.txt", 'w')
f.write("" + listfile + "" + "\n")
f.close()

N = SECP256K1_ORDER
PrivKey = 0x9e636a4ef1a63c4bd385b8d26d29f6394a29963f12109dbf34fef74377866a32

signatures = load_signatures("NoncesHEX.txt")
results = compute_polynonce(signatures, PrivKey, N)
for r in results:
    print("POLYNONCE >> " + r)
