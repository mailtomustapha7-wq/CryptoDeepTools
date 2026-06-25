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
PrivKey = 0xf0a3e31646ce147bbd79bb6e45e6e9c8c4e51c535918c9b4cdca9528eb62172d

signatures = load_signatures("NoncesHEX.txt")
results = compute_polynonce(signatures, PrivKey, N)
for r in results:
    print("POLYNONCE >> " + r)
