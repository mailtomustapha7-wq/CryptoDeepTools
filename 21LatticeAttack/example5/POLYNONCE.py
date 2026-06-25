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
PrivKey = 0xe2eadbde2e6a2adb6f81864cdf574dd44959717fe095486e2c0e55585594edf2

signatures = load_signatures("NoncesHEX.txt")
results = compute_polynonce(signatures, PrivKey, N)
for r in results:
    print("POLYNONCE >> " + r)
