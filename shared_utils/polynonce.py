import csv
from shared_utils.crypto_math import modinv, SECP256K1_ORDER


def format_hex_key(i):
    """Format an integer as a zero-padded 64-character hex string."""
    tmpstr = hex(i)
    hexstr = tmpstr.replace('0x', '').replace('L', '').replace(' ', '').zfill(64)
    return hexstr


def load_signatures(file):
    """Load R, S, Z signature tuples from a CSV file."""
    signatures = []
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            r = int(row[0], 16)
            s = int(row[1], 16)
            z = int(row[2], 16)
            signatures.append((r, s, z))
    return signatures


def compute_polynonce(signatures, priv_key, N=None):
    """Compute and return POLYNONCE values for the given signatures and private key."""
    if N is None:
        N = SECP256K1_ORDER
    results = []
    for r, s, z in signatures:
        zrx = ((z + r * priv_key) % N)
        key = ((zrx * modinv(s, N)) % N)
        results.append(format_hex_key(key))
    return results
