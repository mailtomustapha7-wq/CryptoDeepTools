import sys
import hashlib
from shared_utils import ecdsa_utils as keyUtils
from shared_utils.transaction import parseTxn, getSignableTxn


def extract_ecdsa_params(tx_hex):
    """Parse a raw transaction and extract ECDSA signature parameters R, S, Z and PUBKEY."""
    m = parseTxn(tx_hex)
    e = getSignableTxn(m)

    hash1 = hashlib.sha256(bytes.fromhex(e)).digest()
    hash2 = hashlib.sha256(hash1).digest()

    z = hash2.hex()

    s = keyUtils.derSigToHexSig(m[1][:-2])
    pub = m[2]
    sigR = s[:64]
    sigS = s[-64:]
    sigZ = z

    return sigR, sigS, sigZ, pub
