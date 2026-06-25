import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from shared_utils.signature import extract_ecdsa_params

tx = "" + sys.argv[1]
sigR, sigS, sigZ, pub = extract_ecdsa_params(tx)

print("R = 0x" + sigR)
print("S = 0x" + sigS)
print("Z = 0x" + sigZ)
print("")
print("PUBKEY = " + pub)
print("")
print("======================================================================")
print("")
