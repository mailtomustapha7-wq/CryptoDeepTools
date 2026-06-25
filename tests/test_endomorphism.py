"""
Unit tests for 07EndomorphismSecp256k1/endomorphism.py

Covers: mod, invert, div_nearest, split_scalar_endo,
        JacobianPoint, Point (secp256k1 curve operations)
"""

import sys
import os
import unittest

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "07EndomorphismSecp256k1",
    ),
)

from endomorphism import (
    mod,
    invert,
    div_nearest,
    split_scalar_endo,
    JacobianPoint,
    Point,
    P,
    N,
    GX,
    GY,
    BETA,
    POW_2_128,
)


class TestMod(unittest.TestCase):

    def test_positive_value(self):
        self.assertEqual(mod(10, 7), 3)

    def test_zero(self):
        self.assertEqual(mod(0, 7), 0)

    def test_mod_p_default(self):
        result = mod(P + 5)
        self.assertEqual(result, 5)

    def test_negative_value(self):
        self.assertEqual(mod(-1, 7), 6)

    def test_exact_multiple(self):
        self.assertEqual(mod(14, 7), 0)

    def test_large_value(self):
        self.assertEqual(mod(P, P), 0)
        self.assertEqual(mod(P + 1, P), 1)


class TestInvert(unittest.TestCase):

    def test_invert_1(self):
        self.assertEqual(invert(1, P), 1)

    def test_invert_2(self):
        result = invert(2, P)
        self.assertEqual(mod(2 * result), 1)

    def test_invert_small_prime(self):
        result = invert(3, 7)
        self.assertEqual((3 * result) % 7, 1)

    def test_invert_generator_x(self):
        result = invert(GX, P)
        self.assertEqual(mod(GX * result), 1)

    def test_invert_large_value(self):
        val = 0xDEADBEEF
        result = invert(val, P)
        self.assertEqual(mod(val * result), 1)


class TestDivNearest(unittest.TestCase):

    def test_exact_division(self):
        self.assertEqual(div_nearest(10, 5), 2)

    def test_rounds_to_nearest(self):
        self.assertEqual(div_nearest(7, 2), 4)
        self.assertEqual(div_nearest(5, 2), 3)

    def test_zero_numerator(self):
        self.assertEqual(div_nearest(0, 5), 0)


class TestSplitScalarEndo(unittest.TestCase):

    def test_returns_four_tuple(self):
        result = split_scalar_endo(12345)
        self.assertEqual(len(result), 4)

    def test_components_are_small(self):
        k = 0xDEADBEEFCAFE1234567890ABCDEF
        k1neg, k1, k2neg, k2 = split_scalar_endo(k)
        self.assertIsInstance(k1neg, bool)
        self.assertIsInstance(k2neg, bool)
        self.assertLessEqual(k1, POW_2_128)
        self.assertLessEqual(k2, POW_2_128)

    def test_scalar_1(self):
        k1neg, k1, k2neg, k2 = split_scalar_endo(1)
        self.assertGreater(k1 + k2, 0)

    def test_scalar_n_minus_1(self):
        k1neg, k1, k2neg, k2 = split_scalar_endo(N - 1)
        self.assertLessEqual(k1, POW_2_128)
        self.assertLessEqual(k2, POW_2_128)


class TestJacobianPointZero(unittest.TestCase):

    def test_zero_point(self):
        z = JacobianPoint.zero()
        self.assertEqual(z.x, 0)
        self.assertEqual(z.y, 1)
        self.assertEqual(z.z, 0)

    def test_base_point(self):
        g = JacobianPoint.base()
        self.assertEqual(g.x, GX)
        self.assertEqual(g.y, GY)
        self.assertEqual(g.z, 1)


class TestJacobianPointArithmetic(unittest.TestCase):

    def test_double(self):
        g = JacobianPoint.base()
        g2 = g.double()
        self.assertNotEqual(g2.x, g.x)
        self.assertNotEqual(g2.z, 0)

    def test_add_zero(self):
        g = JacobianPoint.base()
        z = JacobianPoint.zero()
        result = g.add(z)
        self.assertEqual(result.x, g.x)
        self.assertEqual(result.y, g.y)

    def test_add_to_self_equals_double(self):
        g = JacobianPoint.base()
        added = g.add(g)
        doubled = g.double()
        added_affine = added.to_affine()
        doubled_affine = doubled.to_affine()
        self.assertEqual(added_affine.x, doubled_affine.x)
        self.assertEqual(added_affine.y, doubled_affine.y)

    def test_negate(self):
        g = JacobianPoint.base()
        neg_g = g.negate()
        self.assertEqual(neg_g.x, g.x)
        self.assertEqual(mod(-g.y), neg_g.y)
        self.assertEqual(neg_g.z, g.z)


class TestJacobianPointMultiply(unittest.TestCase):

    def test_multiply_by_1(self):
        g = JacobianPoint.base()
        result = g.multiply_unsafe(1)
        affine = result.to_affine()
        self.assertEqual(affine.x, GX)
        self.assertEqual(affine.y, GY)

    def test_multiply_by_2(self):
        g = JacobianPoint.base()
        result = g.multiply_unsafe(2)
        doubled = g.double()
        result_affine = result.to_affine()
        doubled_affine = doubled.to_affine()
        self.assertEqual(result_affine.x, doubled_affine.x)
        self.assertEqual(result_affine.y, doubled_affine.y)

    def test_multiply_known_value(self):
        g = JacobianPoint.base()
        result = g.multiply_unsafe(7)
        affine = result.to_affine()
        expected_x = 0x5CBDF0646E5DB4EAA398F365F2EA7A0E3D419B7E0330E39CE92BDDEDCAC4F9BC
        expected_y = 0x6AEBCA40BA255960A3178D6D861A54DBA813D0B813FDE7B5A5082628087264DA
        self.assertEqual(affine.x, expected_x)
        self.assertEqual(affine.y, expected_y)


class TestPointAffine(unittest.TestCase):

    def test_base_point(self):
        p = Point.base()
        self.assertEqual(p.x, GX)
        self.assertEqual(p.y, GY)

    def test_multiply_scalar_1(self):
        p = Point.base()
        result = p.multiply(1)
        self.assertEqual(result.x, GX)
        self.assertEqual(result.y, GY)

    def test_multiply_scalar_2(self):
        p = Point.base()
        result = p.multiply(2)
        lhs = mod(result.y ** 2)
        rhs = mod(result.x ** 3 + 7)
        self.assertEqual(lhs, rhs)
        jp = JacobianPoint.base()
        jp2 = jp.double()
        affine2 = jp2.to_affine()
        self.assertEqual(result.x, affine2.x)

    def test_multiply_scalar_3(self):
        p = Point.base()
        result = p.multiply(3)
        expected_x = 0xF9308A019258C31049344F85F89D5229B531C845836F99B08601F113BCE036F9
        expected_y = 0x388F7B0F632DE8140FE337E62A37F3566500A99934C2231B6CB9FD7584B8E672
        self.assertEqual(result.x, expected_x)
        self.assertEqual(result.y, expected_y)

    def test_on_curve(self):
        p = Point.base()
        result = p.multiply(42)
        lhs = mod(result.y ** 2)
        rhs = mod(result.x ** 3 + 7)
        self.assertEqual(lhs, rhs)


class TestToFromAffine(unittest.TestCase):

    def test_roundtrip(self):
        p = Point.base()
        jp = JacobianPoint.from_affine(p)
        back = jp.to_affine()
        self.assertEqual(back.x, p.x)
        self.assertEqual(back.y, p.y)

    def test_after_operations(self):
        jp = JacobianPoint.base()
        jp2 = jp.double()
        affine = jp2.to_affine()
        lhs = mod(affine.y ** 2)
        rhs = mod(affine.x ** 3 + 7)
        self.assertEqual(lhs, rhs)
        self.assertNotEqual(affine.x, GX)


if __name__ == "__main__":
    unittest.main()
