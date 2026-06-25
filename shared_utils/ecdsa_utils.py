import ecdsa
import ecdsa.der
import ecdsa.util
import hashlib
import re
import struct
import base58


def privateKeyToWif(key_hex):
    return base58.b58encode_check(b'\x80' + bytes.fromhex(key_hex)).decode('utf-8')


def wifToPrivateKey(s):
    b = base58.b58decode_check(s)
    return b[1:].hex()


def derSigToHexSig(s):
    s_bytes = bytes.fromhex(s)
    s_seq, junk = ecdsa.der.remove_sequence(s_bytes)
    assert junk == b''
    x, s_seq = ecdsa.der.remove_integer(s_seq)
    y, s_seq = ecdsa.der.remove_integer(s_seq)
    return '%064x%064x' % (x, y)


def privateKeyToPublicKey(s):
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(s), curve=ecdsa.SECP256k1)
    return ('04' + sk.verifying_key.to_string().hex())


def keyToAddr(s):
    return pubKeyToAddr(privateKeyToPublicKey(s))


def pubKeyToAddr(s):
    try:
        ripemd160 = hashlib.new('ripemd160')
    except (ValueError, TypeError):
        ripemd160 = hashlib.new('ripemd160', usedforsecurity=False)
    ripemd160.update(hashlib.sha256(bytes.fromhex(s)).digest())
    return base58.b58encode_check(b'\x00' + ripemd160.digest()).decode('utf-8')


def addrHashToScriptPubKey(b58str):
    assert len(b58str) == 34
    decoded = base58.b58decode_check(b58str)
    return '76a914' + decoded[1:].hex() + '88ac'
