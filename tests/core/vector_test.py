import random
import unittest

from core.vector import Vector


class VectorTest(unittest.TestCase):
    zero_vector = Vector(0, 0, 0)
    vector1 = Vector(1, 2, 3)
    vector2 = Vector(4, 5, 6)

    def test_magnitude(self):
        vector = Vector(1, 2, 3)
        magnitude = vector.magnitude()
        self.assertEqual(14, magnitude * magnitude)

        vector = Vector.zero()
        magnitude = vector.magnitude()
        self.assertEqual(0, magnitude * magnitude)

    def test_normalize(self):
        vector = Vector(1, 2, 3)
        magnitude = vector.magnitude()
        normalize = vector.normalize()
        self.assertEqual(vector, normalize * magnitude)

        vector = Vector.zero()
        normalize = vector.normalize()
        self.assertEqual(normalize, Vector.zero())

    def test_scalar_multiplication(self):
        vector = Vector(1, 2, 3)
        scalar = 10
        self.assertEqual(vector * scalar, Vector(10, 20, 30))
        self.assertEqual(scalar * vector, Vector(10, 20, 30))

    def test_scalar_division(self):
        vector = Vector(1, 2, 3)
        self.assertEqual(vector / 10, Vector(0.1, 0.2, 0.3))
        self.assertRaises(ZeroDivisionError, lambda: vector / 0)

    def test_vector_addition(self):
        a = Vector(1, 2, 3)
        b = Vector(2, 3, 1)
        self.assertEqual(a + b, Vector(3, 5, 4))
        self.assertEqual(b + a, Vector(3, 5, 4))

    def test_vector_subtraction(self):
        a = Vector(1, 2, 3)
        b = Vector(2, 3, 1)
        self.assertEqual(a - b, Vector(-1, -1, 2))
        self.assertEqual(b - a, Vector(1, 1, -2))

    def test_vector_equality(self):
        self.assertEqual(Vector(1, 2, 3), Vector(1, 2, 3))

    def test_vector_unary_pos(self):
        a = Vector(1, 2, 3)
        self.assertEqual(Vector(1, 2, 3), +a)

    def test_vector_unary_neg(self):
        vector = Vector(1, 2, 3)
        self.assertEqual(Vector(-1, -2, -3), -vector)

    def test_vector_str(self):
        vector = Vector(1, 2, 3)
        string = str(vector)
        self.assertTrue(
            str(vector.x) in string
            and str(vector.y) in string
            and str(vector.z) in string
        )

    def test_vector_dot_product(self):
        a = Vector(1, 2, 3)
        b = Vector(2, 3, 1)
        self.assertEqual(11, a.scaler_product(b))
        self.assertEqual(11., b.scaler_product(a))

    def test_vector_cross_product(self):
        a = Vector(1, 2, 3)
        b = Vector(2, 3, 1)
        self.assertEqual(Vector(-7, 5, -1), a.vector_product(b))
        self.assertEqual(Vector(7, -5, 1), b.vector_product(a))

    def test_zero_vector(self):
        self.assertEqual(Vector.zero(), Vector(x=0, y=0, z=0), msg="Vector.zero() should return zero vector")
