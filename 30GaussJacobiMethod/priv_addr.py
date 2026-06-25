import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from shared_utils.address import get_address_from_private_key, check_balance

private_key_wif = "5KA4spokBSZ7d5QpcuJ3eTDhNJUhfJoQAUovffQWBym3LP3CKTz"

bitcoin_address = get_address_from_private_key(private_key_wif)
print("__________________________________________________\n")
print(f"Private Key WIF: {private_key_wif}")
print(f"Bitcoin Address: {bitcoin_address}")

check_balance(bitcoin_address)
print("__________________________________________________\n")
