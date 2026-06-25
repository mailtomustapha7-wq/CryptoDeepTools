"""
Unit tests for 04AlgorithmsForSecp256k modules

Covers: EuclideanAlg (Euclide, moduloInverse),
        Helper (reverseBits, moduloPow, EulerCriterion),
        EllipticCurve (ECurve, EPoint)
"""

import sys
import os
import unittest

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "04AlgorithmsForSecp256k",
    ),
)

from EuclideanAlg import Euclide, moduloInverse
from Helper import reverseBits, moduloPow, EulerCriterion, onSameCurve
from EllipticCurve import ECurve, EPoint


class TestEuclide(unittest.TestCase):

    def test_gcd_coprime(self):
        gcd, x, y = Euclide(3, 5)
        self.assertEqual(gcd, 1)
        self.assertEqual(3 * x + 5 * y, 1)

    def test_gcd_common_factor(self):
        gcd, x, y = Euclide(12, 8)
        self.assertEqual(gcd, 4)
        self.assertEqual(12 * x + 8 * y, 4)

    def test_gcd_same_number(self):
        gcd, x, y = Euclide(7, 7)
        self.assertEqual(gcd, 7)

    def test_gcd_one_and_n(self):
        gcd, x, y = Euclide(1, 42)
        self.assertEqual(gcd, 1)

    def test_bezout_identity(self):
        for a, b in [(17, 13), (100, 37), (256, 15)]:
            gcd, x, y = Euclide(a, b)
            self.assertEqual(a * x + b * y, gcd)


class TestModuloInverse(unittest.TestCase):

    def test_inverse_mod_prime(self):
        inv = moduloInverse(3, 7)
        self.assertEqual((3 * inv) % 7, 1)

    def test_inverse_mod_large_prime(self):
        p = 104729
        a = 42
        inv = moduloInverse(a, p)
        self.assertEqual((a * inv) % p, 1)

    def test_inverse_of_1(self):
        self.assertEqual(moduloInverse(1, 7), 1)

    def test_inverse_of_minus_1(self):
        inv = moduloInverse(-1, 7)
        self.assertEqual((-1 * inv) % 7, 1)

    def test_various_primes(self):
        primes = [5, 7, 11, 13, 17, 19, 23, 29, 31]
        for p in primes:
            for a in range(1, p):
                inv = moduloInverse(a, p)
                self.assertEqual((a * inv) % p, 1,
                                 f"Failed for a={a}, p={p}")


class TestReverseBits(unittest.TestCase):

    def test_basic(self):
        rev, n = reverseBits(0b100)
        self.assertEqual(rev, 0b001)
        self.assertEqual(n, 3)

    def test_single_bit(self):
        rev, n = reverseBits(1)
        self.assertEqual(rev, 1)
        self.assertEqual(n, 1)

    def test_palindrome(self):
        rev, n = reverseBits(0b101)
        self.assertEqual(rev, 0b101)
        self.assertEqual(n, 3)

    def test_all_ones(self):
        rev, n = reverseBits(0b1111)
        self.assertEqual(rev, 0b1111)
        self.assertEqual(n, 4)

    def test_larger_value(self):
        rev, n = reverseBits(0b10110)
        self.assertEqual(rev, 0b01101)
        self.assertEqual(n, 5)


class TestModuloPow(unittest.TestCase):

    def test_basic_power(self):
        self.assertEqual(moduloPow(2, 10, 1000), pow(2, 10, 1000))

    def test_power_one(self):
        self.assertEqual(moduloPow(3, 1, 7), 3)

    def test_large_exponent(self):
        result = moduloPow(2, 256, 1000000007)
        expected = pow(2, 256, 1000000007)
        self.assertEqual(result, expected)

    def test_fermat_little_theorem(self):
        p = 17
        for a in range(1, p):
            self.assertEqual(moduloPow(a, p - 1, p), 1)

    def test_small_values(self):
        self.assertEqual(moduloPow(2, 3, 5), pow(2, 3, 5))
        self.assertEqual(moduloPow(5, 7, 13), pow(5, 7, 13))
        self.assertEqual(moduloPow(10, 100, 97), pow(10, 100, 97))


class TestEulerCriterion(unittest.TestCase):

    def test_quadratic_residue(self):
        self.assertTrue(EulerCriterion(1, 7))
        self.assertTrue(EulerCriterion(4, 7))

    def test_non_residue(self):
        self.assertFalse(EulerCriterion(3, 7))

    def test_all_residues_mod_11(self):
        residues = set()
        for i in range(1, 11):
            residues.add((i * i) % 11)
        for r in residues:
            if r != 0:
                self.assertTrue(EulerCriterion(r, 11))

    def test_perfect_square(self):
        self.assertTrue(EulerCriterion(9, 13))


class TestECurve(unittest.TestCase):

    def test_valid_curve(self):
        E = ECurve(2, 3, 97)
        self.assertEqual(E.A, 2)
        self.assertEqual(E.B, 3)
        self.assertEqual(E.mod, 97)

    def test_invalid_mod_raises(self):
        with self.assertRaises(AssertionError):
            ECurve(2, 3, 1)

    def test_invalid_a_negative(self):
        with self.assertRaises(AssertionError):
            ECurve(-1, 3, 97)

    def test_curve_equality(self):
        E1 = ECurve(2, 3, 97)
        E2 = ECurve(2, 3, 97)
        self.assertEqual(E1, E2)

    def test_curve_inequality(self):
        E1 = ECurve(2, 3, 97)
        E2 = ECurve(3, 3, 97)
        self.assertNotEqual(E1, E2)

    def test_string_repr(self):
        E = ECurve(2, 3, 97)
        s = str(E)
        self.assertIn("97", s)
        self.assertIn("2", s)
        self.assertIn("3", s)

    def test_check_curve_params(self):
        self.assertTrue(ECurve.checkCurveParams(2, 3, 97))
        self.assertFalse(ECurve.checkCurveParams(-1, 3, 97))
        self.assertFalse(ECurve.checkCurveParams(2, 3, 0))
        self.assertFalse(ECurve.checkCurveParams(100, 3, 97))


# Pre-computed points on y^2 = x^3 + 2x + 3 (mod 97)
# P = (0, 10), Q = (1, 43), P+Q = (21, 73), 2P = (65, 32)
E_SMALL = ECurve(2, 3, 97)
PX1, PY1 = 0, 10
PX2, PY2 = 1, 43


class TestEPoint(unittest.TestCase):

    def test_point_on_curve(self):
        P = EPoint(E_SMALL, PX1, PY1)
        self.assertEqual(
            (P.y ** 2) % E_SMALL.mod,
            (P.x ** 3 + E_SMALL.A * P.x + E_SMALL.B) % E_SMALL.mod,
        )

    def test_point_addition(self):
        P = EPoint(E_SMALL, PX1, PY1)
        Q = EPoint(E_SMALL, PX2, PY2)
        R = P + Q
        expected = EPoint(E_SMALL, 21, 73)
        self.assertEqual(R, expected)

    def test_point_addition_commutativity(self):
        P = EPoint(E_SMALL, PX1, PY1)
        Q = EPoint(E_SMALL, PX2, PY2)
        self.assertEqual(P + Q, Q + P)

    def test_point_double(self):
        P = EPoint(E_SMALL, PX1, PY1)
        P2 = P + P
        expected = EPoint(E_SMALL, 65, 32)
        self.assertEqual(P2, expected)
        self.assertEqual(P2, 2 * P)

    def test_point_at_infinity(self):
        P = EPoint(E_SMALL, PX1, PY1)
        inf = EPoint(E_SMALL, P.x, P.y, True)
        result = inf + P
        self.assertEqual(result, P)

    def test_add_infinity_right(self):
        P = EPoint(E_SMALL, PX1, PY1)
        inf = EPoint(E_SMALL, P.x, P.y, True)
        result = P + inf
        self.assertEqual(result, P)

    def test_negation(self):
        P = EPoint(E_SMALL, PX1, PY1)
        neg_P = -P
        self.assertEqual(neg_P.x, P.x)
        self.assertEqual(neg_P.y, (-P.y) % E_SMALL.mod)

    def test_scalar_multiplication(self):
        P = EPoint(E_SMALL, PX1, PY1)
        P3 = 3 * P
        P3_manual = P + P + P
        self.assertEqual(P3, P3_manual)

    def test_mul_by_zero(self):
        P = EPoint(E_SMALL, PX1, PY1)
        result = 0 * P
        self.assertTrue(result.inf)

    def test_negative_multiplication(self):
        P = EPoint(E_SMALL, PX1, PY1)
        neg_P = -1 * P
        self.assertEqual(neg_P, -P)

    def test_string_repr_finite(self):
        P = EPoint(E_SMALL, PX1, PY1)
        s = str(P)
        self.assertIn("(", s)
        self.assertIn(")", s)

    def test_string_repr_infinity(self):
        P = EPoint(E_SMALL, PX1, PY1)
        inf = EPoint(E_SMALL, P.x, P.y, True)
        s = str(inf)
        self.assertIn("inf", s)

    def test_hash(self):
        P = EPoint(E_SMALL, PX1, PY1)
        d = {P: "test"}
        self.assertEqual(d[P], "test")

    def test_subtraction(self):
        P = EPoint(E_SMALL, PX1, PY1)
        Q = EPoint(E_SMALL, PX2, PY2)
        diff = P - Q
        self.assertEqual(
            (diff.y ** 2) % E_SMALL.mod,
            (diff.x ** 3 + E_SMALL.A * diff.x + E_SMALL.B) % E_SMALL.mod,
        )


class TestOnSameCurve(unittest.TestCase):

    def test_same_curve(self):
        P = EPoint(E_SMALL, PX1, PY1)
        Q = EPoint(E_SMALL, PX2, PY2)
        self.assertTrue(onSameCurve(P, Q))

    def test_different_curves(self):
        E2 = ECurve(1, 1, 97)
        P = EPoint(E_SMALL, PX1, PY1)
        # Find a point on E2: y^2 = x^3 + x + 1 (mod 97)
        # x=0: f=1, y=1 works (1^2 = 1 mod 97)
        Q = EPoint(E2, 0, 1)
        self.assertFalse(onSameCurve(P, Q))


if __name__ == "__main__":
    unittest.main()
