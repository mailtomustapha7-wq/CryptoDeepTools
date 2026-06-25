"""
Unit tests for 34Vector76Attack/Broadcast-Bitcoin-Transaction-main/sign.py

Covers: hash160, double_sha256, encode_base58, encode_base58_checksum,
        decode_base58, p2pkh_script, p2sh_script, read_varint, encode_varint,
        flip_endian, little_endian_to_int, int_to_little_endian,
        h160_to_p2pkh_address, h160_to_p2sh_address, merkle_parent,
        merkle_parent_level, merkle_root, merkle_path
"""

import hashlib
import math
import sys
import os
import unittest
from binascii import hexlify, unhexlify
from io import BytesIO

try:
    hashlib.new("ripemd160", b"test")
    HAS_RIPEMD160 = True
except (ValueError, Exception):
    HAS_RIPEMD160 = False

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "34Vector76Attack",
        "Broadcast-Bitcoin-Transaction-main",
    ),
)

from sign import (
    hash160,
    double_sha256,
    encode_base58,
    encode_base58_checksum,
    decode_base58,
    p2pkh_script,
    p2sh_script,
    read_varint,
    encode_varint,
    flip_endian,
    little_endian_to_int,
    int_to_little_endian,
    h160_to_p2pkh_address,
    h160_to_p2sh_address,
    merkle_parent,
    merkle_parent_level,
    merkle_root,
    merkle_path,
)


@unittest.skipUnless(HAS_RIPEMD160, "ripemd160 not available in this OpenSSL build")
class TestHash160(unittest.TestCase):

    def test_known_value(self):
        data = b"hello"
        expected = hashlib.new(
            "ripemd160", hashlib.sha256(data).digest()
        ).digest()
        self.assertEqual(hash160(data), expected)

    def test_empty_input(self):
        data = b""
        expected = hashlib.new(
            "ripemd160", hashlib.sha256(data).digest()
        ).digest()
        self.assertEqual(hash160(data), expected)

    def test_returns_20_bytes(self):
        self.assertEqual(len(hash160(b"test data")), 20)


class TestDoubleSha256(unittest.TestCase):

    def test_known_value(self):
        data = b"hello"
        first = hashlib.sha256(data).digest()
        expected = hashlib.sha256(first).digest()
        self.assertEqual(double_sha256(data), expected)

    def test_empty_input(self):
        data = b""
        first = hashlib.sha256(data).digest()
        expected = hashlib.sha256(first).digest()
        self.assertEqual(double_sha256(data), expected)

    def test_returns_32_bytes(self):
        self.assertEqual(len(double_sha256(b"test")), 32)


class TestBase58(unittest.TestCase):

    def test_encode_base58_no_leading_zeros(self):
        raw = bytes.fromhex("7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29")
        result = encode_base58(raw)
        self.assertIsInstance(result, bytes)
        self.assertGreater(len(result), 0)

    def test_encode_base58_with_leading_zeros(self):
        raw = b"\x00\x00" + b"\x01"
        result = encode_base58(raw)
        self.assertTrue(result.startswith(b"11"))

    def test_encode_base58_checksum_returns_string(self):
        data = b"\x00" + b"\x01" * 20
        result = encode_base58_checksum(data)
        self.assertIsInstance(result, str)

    def test_decode_base58_roundtrip(self):
        addr = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        decoded = decode_base58(addr)
        self.assertEqual(len(decoded), 21)
        self.assertEqual(decoded[0], 0)

    def test_decode_base58_bad_checksum(self):
        with self.assertRaises(ValueError):
            decode_base58("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNb")


class TestScripts(unittest.TestCase):

    def test_p2pkh_script_length(self):
        h160 = b"\x01" * 20
        script = p2pkh_script(h160)
        self.assertEqual(len(script), 25)
        self.assertTrue(script.startswith(b"\x76\xa9\x14"))
        self.assertTrue(script.endswith(b"\x88\xac"))

    def test_p2sh_script_length(self):
        h160 = b"\x02" * 20
        script = p2sh_script(h160)
        self.assertEqual(len(script), 23)
        self.assertTrue(script.startswith(b"\xa9\x14"))
        self.assertTrue(script.endswith(b"\x87"))


class TestVarint(unittest.TestCase):

    def test_read_varint_single_byte(self):
        s = BytesIO(bytes([0x42]))
        self.assertEqual(read_varint(s), 0x42)

    def test_read_varint_two_bytes(self):
        s = BytesIO(b"\xfd" + (300).to_bytes(2, "little"))
        self.assertEqual(read_varint(s), 300)

    def test_read_varint_four_bytes(self):
        val = 70000
        s = BytesIO(b"\xfe" + val.to_bytes(4, "little"))
        self.assertEqual(read_varint(s), val)

    def test_read_varint_eight_bytes(self):
        val = 2**33
        s = BytesIO(b"\xff" + val.to_bytes(8, "little"))
        self.assertEqual(read_varint(s), val)

    def test_encode_varint_single(self):
        self.assertEqual(encode_varint(0x42), bytes([0x42]))

    def test_encode_varint_two_bytes(self):
        result = encode_varint(300)
        self.assertEqual(result[0], 0xFD)
        self.assertEqual(little_endian_to_int(result[1:]), 300)

    def test_encode_varint_four_bytes(self):
        result = encode_varint(70000)
        self.assertEqual(result[0], 0xFE)
        self.assertEqual(little_endian_to_int(result[1:]), 70000)

    def test_encode_varint_eight_bytes(self):
        val = 2**33
        result = encode_varint(val)
        self.assertEqual(result[0], 0xFF)
        self.assertEqual(little_endian_to_int(result[1:]), val)

    def test_encode_varint_roundtrip(self):
        for val in [0, 1, 252, 253, 300, 65535, 70000, 2**33]:
            encoded = encode_varint(val)
            decoded = read_varint(BytesIO(encoded))
            self.assertEqual(decoded, val)


class TestEndianConversions(unittest.TestCase):

    def test_flip_endian(self):
        h = "01020304"
        self.assertEqual(flip_endian(h), "04030201")

    def test_flip_endian_single_byte(self):
        self.assertEqual(flip_endian("ab"), "ab")

    def test_little_endian_to_int(self):
        self.assertEqual(little_endian_to_int(b"\x01\x00"), 1)
        self.assertEqual(little_endian_to_int(b"\xff\x00"), 255)
        self.assertEqual(little_endian_to_int(b"\x00\x01"), 256)

    def test_int_to_little_endian(self):
        self.assertEqual(int_to_little_endian(1, 2), b"\x01\x00")
        self.assertEqual(int_to_little_endian(256, 4), b"\x00\x01\x00\x00")

    def test_endian_roundtrip(self):
        for val in [0, 1, 255, 256, 65535, 2**24]:
            le_bytes = int_to_little_endian(val, 4)
            self.assertEqual(little_endian_to_int(le_bytes), val)


@unittest.skipUnless(HAS_RIPEMD160, "ripemd160 not available in this OpenSSL build")
class TestAddressConversions(unittest.TestCase):

    def test_h160_to_p2pkh_address(self):
        h160 = hash160(b"\x04" + b"\x01" * 64)
        addr = h160_to_p2pkh_address(h160)
        self.assertIsInstance(addr, str)
        self.assertTrue(addr.startswith("1"))

    def test_h160_to_p2sh_address(self):
        h160 = hash160(b"\x04" + b"\x02" * 64)
        addr = h160_to_p2sh_address(h160)
        self.assertIsInstance(addr, str)
        self.assertTrue(addr.startswith("3"))

    def test_p2pkh_testnet_prefix(self):
        h160 = hash160(b"test")
        addr = h160_to_p2pkh_address(h160, prefix=b"\x6f")
        self.assertIsInstance(addr, str)


class TestMerkle(unittest.TestCase):

    def test_merkle_parent(self):
        h1 = bytes.fromhex("c117ea8ec828342f4dfb0ad6bd140e03a50720ece40169ee38bdc15d9eb64cf5")
        h2 = bytes.fromhex("c131474164b412e3406696da1ee20ab0fc9bf41c8f05fa8ceea7a08d672d7cc5")
        parent = merkle_parent(h1, h2)
        self.assertEqual(len(parent), 32)
        expected = double_sha256(h1 + h2)
        self.assertEqual(parent, expected)

    def test_merkle_parent_level_even(self):
        hashes = [b"\x01" * 32, b"\x02" * 32, b"\x03" * 32, b"\x04" * 32]
        result = merkle_parent_level(hashes)
        self.assertEqual(len(result), 2)

    def test_merkle_parent_level_odd(self):
        hashes = [b"\x01" * 32, b"\x02" * 32, b"\x03" * 32]
        result = merkle_parent_level(hashes)
        self.assertEqual(len(result), 2)

    def test_merkle_parent_level_single_raises(self):
        with self.assertRaises(RuntimeError):
            merkle_parent_level([b"\x01" * 32])

    def test_merkle_root_single(self):
        hashes = [b"\xab" * 32]
        self.assertEqual(merkle_root(hashes), b"\xab" * 32)

    def test_merkle_root_two(self):
        h1 = b"\x01" * 32
        h2 = b"\x02" * 32
        root = merkle_root([h1, h2])
        self.assertEqual(root, double_sha256(h1 + h2))

    def test_merkle_root_four(self):
        hashes = [bytes([i]) * 32 for i in range(4)]
        root = merkle_root(hashes)
        self.assertEqual(len(root), 32)

    def test_merkle_path(self):
        path = merkle_path(3, 8)
        self.assertEqual(len(path), 3)
        self.assertEqual(path[0], 3)


if __name__ == "__main__":
    unittest.main()
