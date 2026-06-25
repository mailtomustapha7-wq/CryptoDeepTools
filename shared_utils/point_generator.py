import sys
from ecpy.curves import Curve, Point

SECP256K1_CURVE = Curve.get_curve('secp256k1')
SECP256K1_GENERATOR = Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8,
    SECP256K1_CURVE,
)


def generate_point(k_hex):
    """Multiply the secp256k1 generator by scalar k (given as hex string) and return the resulting point."""
    k = int(k_hex, 16)
    return k * SECP256K1_GENERATOR
