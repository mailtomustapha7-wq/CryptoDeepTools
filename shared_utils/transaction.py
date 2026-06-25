import ecdsa
import hashlib
import struct
import base58
from shared_utils import ecdsa_utils as keyUtils


def makeRawTransaction(outputTransactionHash, sourceIndex, scriptSig, outputs):
    def makeOutput(data):
        redemptionSatoshis, outputScript = data
        return (struct.pack("<Q", redemptionSatoshis).hex() +
                '%02x' % len(bytes.fromhex(outputScript)) + outputScript)

    formattedOutputs = ''.join(map(makeOutput, outputs))

    return ("01000000" +
            "01" +
            bytes.fromhex(outputTransactionHash)[::-1].hex() +
            struct.pack('<L', sourceIndex).hex() +
            '%02x' % len(bytes.fromhex(scriptSig)) + scriptSig +
            "ffffffff" +
            "%02x" % len(outputs) +
            formattedOutputs +
            "00000000")


def parseTxn(txn):
    first = txn[0:41 * 2]
    scriptLen = int(txn[41 * 2:42 * 2], 16)
    script = txn[42 * 2:42 * 2 + 2 * scriptLen]
    sigLen = int(script[0:2], 16)
    sig = script[2:2 + sigLen * 2]
    pubLen = int(script[2 + sigLen * 2:2 + sigLen * 2 + 2], 16)
    pub = script[2 + sigLen * 2 + 2:]
    assert len(pub) == pubLen * 2
    rest = txn[42 * 2 + 2 * scriptLen:]
    return [first, sig, pub, rest]


def getSignableTxn(parsed):
    first, sig, pub, rest = parsed
    inputAddr = base58.b58decode_check(keyUtils.pubKeyToAddr(pub))
    return first + "1976a914" + inputAddr.hex() + "88ac" + rest + "01000000"


def verifyTxnSignature(txn):
    parsed = parseTxn(txn)
    signableTxn = getSignableTxn(parsed)

    hash1 = hashlib.sha256(bytes.fromhex(signableTxn)).digest()
    hashToSign = hashlib.sha256(hash1).hexdigest()

    assert parsed[1][-2:] == '01'

    sig = keyUtils.derSigToHexSig(parsed[1][:-2])
    public_key = parsed[2]

    vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key[2:]), curve=ecdsa.SECP256k1)
    assert vk.verify_digest(bytes.fromhex(sig), bytes.fromhex(hashToSign))


def makeSignedTransaction(privateKey, outputTransactionHash, sourceIndex, scriptPubKey, outputs):
    myTxn_forSig = (makeRawTransaction(outputTransactionHash, sourceIndex, scriptPubKey, outputs)
                    + "01000000")

    s256 = hashlib.sha256(hashlib.sha256(bytes.fromhex(myTxn_forSig)).digest()).digest()

    sk = ecdsa.SigningKey.from_string(bytes.fromhex(privateKey), curve=ecdsa.SECP256k1)
    sig = sk.sign_digest(s256, sigencode=ecdsa.util.sigencode_der) + b'\x01'

    pubKey = keyUtils.privateKeyToPublicKey(privateKey)

    def varstr(s):
        return bytes([len(s)]) + s

    scriptSig = varstr(sig).hex() + varstr(bytes.fromhex(pubKey)).hex()

    signed_txn = makeRawTransaction(outputTransactionHash, sourceIndex, scriptSig, outputs)
    verifyTxnSignature(signed_txn)
    return signed_txn
