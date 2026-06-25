import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from shared_utils.address import decode_base58

if __name__ == "__main__":
    address = input("Enter Bitcoin address:  ")
    decoded_bytes = decode_base58(address)
    print("Bitcoin HASH160: ", decoded_bytes.hex())

