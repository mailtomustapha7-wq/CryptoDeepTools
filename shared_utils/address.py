import hashlib
import sys
import re
from time import sleep

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

import base58


def hash160(hex_str):
    sha = hashlib.sha256()
    sha.update(hex_str)
    try:
        rip = hashlib.new('ripemd160')
    except (ValueError, TypeError):
        # On OpenSSL 3.x, ripemd160 may be disabled by default; enable legacy provider
        rip = hashlib.new('ripemd160', usedforsecurity=False)
    rip.update(sha.digest())
    return rip.hexdigest()


def decode_base58(address):
    decoded = base58.b58decode(address)
    return decoded[1:-4]


def pubkey_to_address(pub_key_hex, compress=False, input_file=None, output_file=None):
    """Convert a single public key hex string to a Bitcoin address.

    If input_file and output_file are provided, batch-converts all public keys
    from input_file and writes addresses to output_file.
    """
    if input_file and output_file:
        pub_keys = open(input_file, 'r', encoding='utf-8')
        new_file = open(output_file, 'a', encoding='utf-8')
        for pub_key in pub_keys:
            pub_key = pub_key.replace('\n', '')
            addr = _single_pubkey_to_address(pub_key, compress)
            new_file.write(addr + "\n")
        pub_keys.close()
        new_file.close()
        return None

    return _single_pubkey_to_address(pub_key_hex, compress)


def _single_pubkey_to_address(pub_key_hex, compress=False):
    if compress:
        if ord(bytearray.fromhex(pub_key_hex[-2:])) % 2 == 0:
            pubkey_compressed = '02'
        else:
            pubkey_compressed = '03'
        pubkey_compressed += pub_key_hex[2:66]
        hex_str = bytearray.fromhex(pubkey_compressed)
    else:
        hex_str = bytearray.fromhex(pub_key_hex)

    key_hash = '00' + hash160(hex_str)

    sha = hashlib.sha256()
    sha.update(bytearray.fromhex(key_hash))
    checksum = sha.digest()
    sha = hashlib.sha256()
    sha.update(checksum)
    checksum = sha.hexdigest()[0:8]

    return base58.b58encode(bytes(bytearray.fromhex(key_hash + checksum))).decode('utf-8')


def get_address_from_private_key(private_key_wif):
    from bitcoin import decode_privkey, privtopub, pubtoaddr
    private_key = decode_privkey(private_key_wif)
    public_key = privtopub(private_key)
    address = pubtoaddr(public_key)
    return address


def check_balance(address):
    SONG_BELL = True
    WARN_WAIT_TIME = 0
    SATOSHIS_PER_BTC = 1e+8

    blockchain_tags_json = ['total_received']

    check_address = address
    parse_address_structure = re.match(r' *([a-zA-Z1-9]{1,34})', check_address)
    if parse_address_structure is not None:
        check_address = parse_address_structure.group(1)
    else:
        exit(1)

    reading_state = 1
    while reading_state:
        try:
            htmlfile = urlopen("https://blockchain.info/address/%s?format=json" % check_address, timeout=10)
            htmltext = htmlfile.read().decode('utf-8')
            reading_state = 0
        except Exception:
            reading_state += 1
            print("Checking... " + str(reading_state))
            sleep(60 * reading_state)

    blockchain_info_array = []
    tag = ''
    try:
        for tag in blockchain_tags_json:
            blockchain_info_array.append(
                float(re.search(r'%s":(\d+),' % tag, htmltext).group(1)))
    except Exception:
        print("Error '%s'." % tag)
        exit(1)

    for i, btc_tokens in enumerate(blockchain_info_array):
        sys.stdout.write("%s \t= " % blockchain_tags_json[i])
        if btc_tokens > 0.0:
            print("%.8f Bitcoin" % (btc_tokens / SATOSHIS_PER_BTC))
        else:
            print("0 Bitcoin")

        if SONG_BELL and blockchain_tags_json[i] == 'final_balance' and btc_tokens > 0.0:
            sys.stdout.write('\a\a\a')
            sys.stdout.flush()

            with open('balance.json', 'a') as arq1:
                arq1.write("Bitcoin Address: %s" % check_address)
                arq1.write("\t Balance: %.8f Bitcoin" % (btc_tokens / SATOSHIS_PER_BTC))
                arq1.write("\n")

            if WARN_WAIT_TIME > 0:
                sleep(WARN_WAIT_TIME)
