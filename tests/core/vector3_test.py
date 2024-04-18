import random
import unittest

from core.vector3 import Vector


class Vector3Test(unittest.TestCase):

    zero_vector = Vector(0, 0, 0)
    vector1 = Vector(1, 2, 3)
    vector2 = Vector(4, 5, 6)

    def test_zero_vector(self):
        self.assertTrue(Vector.zero() == Vector(x=0, y=0, z=0), msg="Vector.zero() should return zero vector")

    def test_negative_vector(self):
        for vector in [self.zero_vector, self.vector1, self.vector2]:
            self.assertEqual(
                Vector(-vector.x, -vector.y, -vector.z),
                -vector,
                msg="'-' should return negative vector"
            )

    def test_vector_scaler_multiplication(self):
        for vector in [self.zero_vector, self.vector1, self.vector2]:
            scaler = random.random()
            self.assertEqual(
                Vector(scaler * vector.x, scaler * vector.y, scaler * vector.z),
                vector * scaler,
                msg="should return scaled vector"
            )
            self.assertEqual(
                Vector(scaler * vector.x, scaler * vector.y, scaler * vector.z),
                scaler * vector,
                msg="should return scaled vector"
            )

    def test_vector_addition(self):
        self.assertEqual(Vector(1, 2, 3) + Vector(4, 5, 6), Vector(5, 7, 9),
                         msg="Vector.add() should return vector addition")

    def test_vector_subtraction(self):
        self.assertEqual(Vector(1, 2, 3) - Vector(4, 5, 6), Vector(-3, -3, -3),
                         msg="Vector.subtract() should return vector subtraction")

    def test_vector_component_product(self):
        self.assertEqual(Vector(1, 2, 3).scaler_product(Vector(4, 5, 6)),
                         4 + 10 + 18,
                         msg="Vector.component_product() should return vector component product")

    def test_vector_vector_product(self):
        self.assertEqual(Vector(1, 2, 3).vector_product(Vector(4, 5, 6)),
                         Vector(-3, 6, -3),
                         msg="Vector.vector_product() should return vector vector product")


