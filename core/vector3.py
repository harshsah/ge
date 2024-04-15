import math


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
                 x: float,
                 y: float,
                 z: float,
                 ):
        self.x = x
        self.y = y
        self.z = z
        # self._pad = 0.0

    def _square_magnitude(self) -> float:
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def magnitude(self) -> float:
        """
        Returns the magnitude of the vector (x^2 + y^2 + z^2) ^ 0.5
        """
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self) -> 'Vector':
        """
        Returns the normalized vector (x / sqrt(x^2 + y^2 + z^2)) or zero vector in case of zero magnitude.
        """
        m = self.magnitude()
        if m > 0:
            return self / m
        return self

    def __mul__(self, scaler: float) -> 'Vector':
        """
        Multiplies the vector by a scalar.
        :param scaler: scalar multiplier for the vector
        :type scaler: float
        """
        return Vector(self.x * scaler, self.y * scaler, self.z * scaler)

    def __rmul__(self, scaler: float) -> 'Vector':
        """
        Multiplies the vector by a scalar.
        :param scaler:
        :type scaler: float
        """
        return self * scaler

    def __add__(self, other: 'Vector') -> 'Vector':
        """
        Adds two vectors together
        (self.x + other.x, self.y + other.y, self.z + other.z)
        :param other: other vector to add
        :type other: Vector
        """
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector') -> 'Vector':
        """
        Subtracts two vectors together
        (self.x - other.x, self.y - other.y, self.z - other.z)
        :param other: other to subtract
        :type other: Vector
        """
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __eq__(self, other: 'Vector') -> bool:
        """
        Checks if the vector is equal to another vector
        (self.x == other.x and self.y == other.y and self.z == other.z).
        :param other: vector to compare
        :type other: Vector
        """
        return self.x == other.x and self.y == other.y and self.z == other.z


    def __pos__(self) -> 'Vector':
        """
        Returns itself
        """
        return self

    def __neg__(self) -> 'Vector':
        """
        Returns the negation/invert of the vector.
        (-self.x, -self.y, -self.z)
        """
        return Vector(self.x * -1, self.y * -1, self.z * -1)

    def __str__(self) -> str:
        """
        Returns the string representation of the vector.
        (self.x, self.y, self.z)
        """
        return f'({self.x}, {self.y}, {self.z})'

    def scaler_product(self, other: 'Vector') -> float:
        """
        Returns the component product of two vectors.
        :param other: other vector for component product
        :type other: Vector
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def vector_product(self, other: 'Vector') -> 'Vector':
        """
        Returns the vector product of two vectors.
        (
        self.y * other.z - self.z * other.y,
        self.z * other.x - self.x * other.z,
        self.x * other.y - self.y * other.x
        )
        :param other: other vector for scalar product
        :type other: Vector
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
        (0, 0, 0)
        """
        return Vector(0., 0., 0.)
