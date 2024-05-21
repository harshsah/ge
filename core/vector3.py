import math
import random

VECTOR_COMPARISON_EPSILON = 0.001


class Vector:
    """
    A class to represent a vector in 3D space.

    :param x: the x component of the vector
    :type x: float
    :param y: the y component of the vector
    :type y: float
    :param z: the z component of the vector
    :type z: float
    """

    def __init__(self,
                 x: float = 0.0,
                 y: float = 0.0,
                 z: float = 0.0,
                 ):
        self.x = x
        self.y = y
        self.z = z

    def _square_magnitude(self) -> float:
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def magnitude(self) -> float:
        """
        :return: the magnitude of the vector (x^2 + y^2 + z^2) ^ 0.5
        """
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self) -> 'Vector':
        """
        :return: the normalized vector (x / sqrt(x^2 + y^2 + z^2)) or zero vector in case of zero magnitude.
        """
        m = self.magnitude()
        if m > 0:
            return self / m
        return self

    def __mul__(self, scaler: float) -> 'Vector':
        """
        Multiplies the vector by a scalar.

        :param scaler: the scaler
        :type scaler: float

        :return: the multiplied vector (x * scaler, y * scaler, z * scaler)
        """
        return Vector(self.x * scaler, self.y * scaler, self.z * scaler)

    def __rmul__(self, scaler: float) -> 'Vector':
        """
        Multiplies the vector by a scalar.

        :param scaler: the scaler
        :type scaler: float

        :return: the multiplied vector (x * scaler, y * scaler, z * scaler)
        """
        return self * scaler

    def __truediv__(self, scaler: float) -> 'Vector':
        """
        Divides the vector by a scalar.
        :param scaler: the scaler of the vec
        :type scaler: float
        :return: the divided vector (x / scaler, y / scaler, z / scaler)
        :raise ZeroDivisionError: if the scaler is zero
        """
        if scaler == 0:
            raise ZeroDivisionError("Scaler cannot be zero")
        return Vector(self.x / scaler, self.y / scaler, self.z / scaler)

    def __add__(self, other: 'Vector') -> 'Vector':
        """
        Adds two vectors together

        :param other: the vector to add
        :type other: Vector

        :return: the added vector (self.x + other.x, self.y + other.y, self.z + other.z)
        """
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector') -> 'Vector':
        """
        Subtracts two vectors together

        :param other: the vector to subtract
        :type other: Vector

        :return: the subtracted vector (self.x - other.x, self.y - other.y, self.z - other.z)
        """
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __eq__(self, other: 'Vector') -> bool:
        """
        Checks if the vector is equal to another vector

        :param other: the vector to check
        :type other: Vector

        :return: True if the vector is equal to another vector, False otherwise
        (self.x == other.x and self.y == other.y and self.z == other.z)

        """
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        diff = self - other
        diff = diff / (self.magnitude() + other.magnitude())
        return diff.magnitude() < VECTOR_COMPARISON_EPSILON

    def __pos__(self) -> 'Vector':
        """
        :return: copy of itself
        """
        return Vector(self.x, self.y, self.z)

    def __neg__(self) -> 'Vector':
        """
        Returns the negation/invert of the vector.

        :return: the negation/invert of the vector (-self.x, -self.y, -self.z)
        """
        return Vector(self.x * -1, self.y * -1, self.z * -1)

    def __str__(self) -> str:
        """
        Returns the string representation of the vector.

        :return: the string representation of the vector (self.x, self.y, self.z)
        """
        return f'({self.x}, {self.y}, {self.z})'

    def scaler_product(self, other: 'Vector') -> float:
        """
        Returns the component product of two vectors.
        :param other: other vector for component product
        :type other: Vector

        :return: the component product, self.x * other.x + self.y * other.y + self.z * other.z
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def vector_product(self, other: 'Vector') -> 'Vector':
        """
        Returns the vector product of two vectors.

        :param other: other vector for component product
        :type other: Vector

        :return: the vector product (
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x
            )
        """
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    @staticmethod
    def zero() -> 'Vector':
        """
        Returns the zero vector.

        :return: the zero vector (0, 0, 0)
        """
        return Vector(0., 0., 0.)

    @staticmethod
    def random() -> 'Vector':
        """
        Returns a random vector with each coordinate range [0, 1).
        :return: a random vector
        """
        return Vector(random.random(), random.random(), random.random())
