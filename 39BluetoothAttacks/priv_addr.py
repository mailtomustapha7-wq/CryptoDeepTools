import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from shared_utils.address import get_address_from_private_key, check_balance

private_key_wif = "12d3428123e4262d6890e0ef149ce3c1335229b3f44ed6026bdec2921e796d34"

bitcoin_address = get_address_from_private_key(private_key_wif)
print("__________________________________________________\n")
print(f"Private Key WIF: {private_key_wif}")
print(f"Bitcoin Address: {bitcoin_address}")

check_balance(bitcoin_address)
print("__________________________________________________\n")
