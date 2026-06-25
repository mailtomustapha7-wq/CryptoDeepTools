import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from bitcoin import privtopub, encode_pubkey, pubtoaddr

with open("PrivateKey.txt", "r") as f:
    content = f.readlines()

content = [x.strip() for x in content]

outfile = open("PrivateKeyAddr.txt", "w")
for x in content:
    outfile.write(x + ":" + pubtoaddr(encode_pubkey(privtopub(x), "bin_compressed")) + "\n")

outfile.close()

