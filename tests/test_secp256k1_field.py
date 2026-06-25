"""
Unit tests for 34Vector76Attack/Broadcast-Bitcoin-Transaction-main/secp256k1.py

Covers: FieldElement, Point, S256Field, S256Point, Signature
"""

import sys
import os
import unittest
from binascii import hexlify

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "34Vector76Attack",
        "Broadcast-Bitcoin-Transaction-main",
    ),
)

from secp256k1 import (
    FieldElement,
    Point,
    S256Field,
    S256Point,
    Signature,
    G,
    A,
    B,
    P,
    N,
)


class TestFieldElement(unittest.TestCase):

    def test_create_valid(self):
        fe = FieldElement(5, 7)
        self.assertEqual(fe.num, 5)
        self.assertEqual(fe.prime, 7)

    def test_create_out_of_range(self):
        with self.assertRaises(RuntimeError):
            FieldElement(7, 7)
        with self.assertRaises(RuntimeError):
            FieldElement(-1, 7)

    def test_equality(self):
        a = FieldElement(3, 7)
        b = FieldElement(3, 7)
        self.assertEqual(a, b)

    def test_inequality(self):
        a = FieldElement(3, 7)
        b = FieldElement(4, 7)
        self.assertNotEqual(a, b)

    def test_ne_none(self):
        a = FieldElement(3, 7)
        self.assertNotEqual(a, None)

    def test_add(self):
        a = FieldElement(3, 7)
        b = FieldElement(5, 7)
        result = a + b
        self.assertEqual(result, FieldElement(1, 7))

    def test_add_different_primes(self):
        a = FieldElement(3, 7)
        b = FieldElement(3, 11)
        with self.assertRaises(RuntimeError):
            a + b

    def test_sub(self):
        a = FieldElement(3, 7)
        b = FieldElement(5, 7)
        result = a - b
        self.assertEqual(result, FieldElement(5, 7))

    def test_mul(self):
        a = FieldElement(3, 7)
        b = FieldElement(4, 7)
        result = a * b
        self.assertEqual(result, FieldElement(5, 7))

    def test_rmul(self):
        a = FieldElement(3, 7)
        result = 2 * a
        self.assertEqual(result, FieldElement(6, 7))

    def test_pow(self):
        a = FieldElement(3, 7)
        result = a ** 2
        self.assertEqual(result, FieldElement(2, 7))

    def test_pow_fermat(self):
        a = FieldElement(3, 7)
        result = a ** 6
        self.assertEqual(result, FieldElement(1, 7))

    def test_div(self):
        a = FieldElement(2, 7)
        b = FieldElement(3, 7)
        result = a / b
        self.assertEqual(result.num, (2 * pow(3, 5, 7)) % 7)

    def test_repr(self):
        a = FieldElement(3, 7)
        self.assertEqual(repr(a), "FieldElement_7(3)")


class TestPoint(unittest.TestCase):

    def test_point_at_infinity(self):
        p = Point(None, None, FieldElement(0, 7), FieldElement(5, 7))
        self.assertIsNone(p.x)
        self.assertIsNone(p.y)

    def test_valid_point(self):
        a = FieldElement(0, 223)
        b = FieldElement(7, 223)
        x = FieldElement(192, 223)
        y = FieldElement(105, 223)
        p = Point(x, y, a, b)
        self.assertEqual(p.x, x)
        self.assertEqual(p.y, y)

    def test_invalid_point_raises(self):
        a = FieldElement(0, 223)
        b = FieldElement(7, 223)
        x = FieldElement(200, 223)
        y = FieldElement(119, 223)
        with self.assertRaises(RuntimeError):
            Point(x, y, a, b)

    def test_add_identity(self):
        a = FieldElement(0, 223)
        b = FieldElement(7, 223)
        x = FieldElement(192, 223)
        y = FieldElement(105, 223)
        p = Point(x, y, a, b)
        inf = Point(None, None, a, b)
        self.assertEqual(p + inf, p)
        self.assertEqual(inf + p, p)

    def test_add_two_points(self):
        a = FieldElement(0, 223)
        b = FieldElement(7, 223)
        p1 = Point(FieldElement(192, 223), FieldElement(105, 223), a, b)
        p2 = Point(FieldElement(17, 223), FieldElement(56, 223), a, b)
        result = p1 + p2
        expected = Point(FieldElement(170, 223), FieldElement(142, 223), a, b)
        self.assertEqual(result, expected)

    def test_add_vertical_line(self):
        a = FieldElement(0, 223)
        b = FieldElement(7, 223)
        p1 = Point(FieldElement(192, 223), FieldElement(105, 223), a, b)
        neg_y = FieldElement((223 - 105) % 223, 223)
        p2 = Point(FieldElement(192, 223), neg_y, a, b)
        result = p1 + p2
        self.assertIsNone(result.x)

    def test_double(self):
        a = FieldElement(0, 223)
        b = FieldElement(7, 223)
        p = Point(FieldElement(192, 223), FieldElement(105, 223), a, b)
        result = p + p
        self.assertIsNotNone(result.x)

    def test_rmul(self):
        a = FieldElement(0, 223)
        b = FieldElement(7, 223)
        p = Point(FieldElement(192, 223), FieldElement(105, 223), a, b)
        result = 2 * p
        expected = p + p
        self.assertEqual(result, expected)

    def test_different_curves_raises(self):
        a1 = FieldElement(0, 223)
        b1 = FieldElement(7, 223)
        a2 = FieldElement(1, 223)
        b2 = FieldElement(7, 223)
        p1 = Point(FieldElement(192, 223), FieldElement(105, 223), a1, b1)
        p2 = Point(None, None, a2, b2)
        with self.assertRaises(RuntimeError):
            p1 + p2


class TestS256Field(unittest.TestCase):

    def test_creation(self):
        f = S256Field(42)
        self.assertEqual(f.num, 42)
        self.assertEqual(f.prime, P)

    def test_hex(self):
        f = S256Field(255)
        h = f.hex()
        self.assertEqual(len(h), 64)
        self.assertTrue(h.endswith("ff"))

    def test_sqrt(self):
        f = S256Field(4)
        result = f.sqrt()
        self.assertEqual(result ** 2, f)


class TestS256Point(unittest.TestCase):

    def test_generator_on_curve(self):
        self.assertIsNotNone(G.x)
        self.assertIsNotNone(G.y)

    def test_generator_order(self):
        result = N * G
        self.assertIsNone(result.x)

    def test_point_at_infinity(self):
        inf = S256Point(None, None)
        self.assertIsNone(inf.x)

    def test_add_generator_to_itself(self):
        result = G + G
        self.assertIsNotNone(result.x)
        self.assertNotEqual(result.x, G.x)

    def test_scalar_mul_consistency(self):
        result2 = 2 * G
        result_add = G + G
        self.assertEqual(result2, result_add)

    def test_sec_compressed_even(self):
        point = 2 * G
        sec = point.sec(compressed=True)
        self.assertEqual(len(sec), 33)
        self.assertIn(sec[0], [2, 3])

    def test_sec_uncompressed(self):
        sec = G.sec(compressed=False)
        self.assertEqual(len(sec), 65)
        self.assertEqual(sec[0], 4)

    def test_parse_uncompressed(self):
        sec = G.sec(compressed=False)
        parsed = S256Point.parse(sec)
        self.assertEqual(parsed, G)

    def test_parse_compressed(self):
        sec = G.sec(compressed=True)
        parsed = S256Point.parse(sec)
        self.assertEqual(parsed, G)

    def test_repr_infinity(self):
        inf = S256Point(None, None)
        self.assertEqual(repr(inf), "Point(infinity)")

    def test_repr_finite(self):
        r = repr(G)
        self.assertTrue(r.startswith("Point("))


class TestSignature(unittest.TestCase):

    def test_creation(self):
        sig = Signature(1, 2)
        self.assertEqual(sig.r, 1)
        self.assertEqual(sig.s, 2)

    def test_repr(self):
        sig = Signature(0xDEAD, 0xBEEF)
        r = repr(sig)
        self.assertIn("dead", r)
        self.assertIn("beef", r)

    def test_der_encoding(self):
        sig = Signature(
            0x37206A0610995C58074999CB9767B87AF4C4978DB68C06E8E6E81D282047A7C6,
            0x8CA63759C1157EBEAEC0D03CECCA119FC9A75BF8E6D0FA65C841C8E2738CDAEC,
        )
        der = sig.der()
        self.assertEqual(der[0], 0x30)
        self.assertGreater(len(der), 0)

    def test_der_parse_roundtrip(self):
        sig = Signature(
            0x37206A0610995C58074999CB9767B87AF4C4978DB68C06E8E6E81D282047A7C6,
            0x8CA63759C1157EBEAEC0D03CECCA119FC9A75BF8E6D0FA65C841C8E2738CDAEC,
        )
        der = sig.der()
        parsed = Signature.parse(der)
        self.assertEqual(parsed.r, sig.r)
        self.assertEqual(parsed.s, sig.s)

    def test_der_bad_marker(self):
        with self.assertRaises(RuntimeError):
            Signature.parse(b"\x31\x06\x02\x01\x01\x02\x01\x02")


if __name__ == "__main__":
    unittest.main()
