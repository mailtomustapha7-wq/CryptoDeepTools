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
PrivKey = 0xff0178fa717374f7e74d43f00150748967ea04b64241ec10a10f62debb70868c

signatures = load_signatures("NoncesHEX.txt")
results = compute_polynonce(signatures, PrivKey, N)
for r in results:
    print("POLYNONCE >> " + r)
