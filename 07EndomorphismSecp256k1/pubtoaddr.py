import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from shared_utils.address import pubkey_to_address

pubkey_to_address(None, compress=False, input_file='pubkey.txt', output_file='BitcoinAddress.txt')
