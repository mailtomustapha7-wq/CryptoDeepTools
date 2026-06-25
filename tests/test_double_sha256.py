"""
Unit tests for 38QuantumAttacks/DoubleSHA256Hasher.py

Covers: double_sha256 function
"""

import hashlib
import sys
import os
import unittest

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "38QuantumAttacks",
    ),
)

from DoubleSHA256Hasher import double_sha256


class TestDoubleSHA256Hasher(unittest.TestCase):

    def test_known_value(self):
        data = b"hello"
        h1 = hashlib.sha256(data).digest()
        expected = hashlib.sha256(h1).digest()
        self.assertEqual(double_sha256(data), expected)

    def test_empty_input(self):
        data = b""
        h1 = hashlib.sha256(data).digest()
        expected = hashlib.sha256(h1).digest()
        self.assertEqual(double_sha256(data), expected)

    def test_returns_32_bytes(self):
        result = double_sha256(b"test")
        self.assertEqual(len(result), 32)

    def test_different_inputs_different_hashes(self):
        self.assertNotEqual(double_sha256(b"abc"), double_sha256(b"abd"))

    def test_deterministic(self):
        data = b"CryptoDeepTools"
        self.assertEqual(double_sha256(data), double_sha256(data))

    def test_bitcoin_block_header_example(self):
        data = b"Example data for double SHA256"
        result = double_sha256(data)
        self.assertIsInstance(result, bytes)
        self.assertEqual(len(result), 32)
        hex_result = result.hex()
        self.assertEqual(len(hex_result), 64)

    def test_single_byte(self):
        result = double_sha256(b"\x00")
        expected = hashlib.sha256(hashlib.sha256(b"\x00").digest()).digest()
        self.assertEqual(result, expected)

    def test_large_input(self):
        data = b"A" * 10000
        result = double_sha256(data)
        expected = hashlib.sha256(hashlib.sha256(data).digest()).digest()
        self.assertEqual(result, expected)

    def test_not_single_sha256(self):
        data = b"test"
        single = hashlib.sha256(data).digest()
        double = double_sha256(data)
        self.assertNotEqual(single, double)

    def test_hex_output(self):
        data = b"Example data for double SHA256"
        result = double_sha256(data)
        hex_str = result.hex()
        self.assertTrue(all(c in "0123456789abcdef" for c in hex_str))


if __name__ == "__main__":
    unittest.main()
