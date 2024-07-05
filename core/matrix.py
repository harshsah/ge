from core.vector import Vector


class Matrix3:
    """
    Holds an inertia tensor, consisting of a 3x3 row-major matrix. This is not padding to produce an aligned structure,
    since it is most commonly used with a mass (single real) and two damping coefficients to make the 12-element
    characteristics array of a rigid body

    :param data: holds the tensor matrix data in array form
    """

    def __init__(self,
                 data: list[float] = None):
        if data is None:
            data = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.data = data

    def __mul__(self, o: 'Matrix3'):
        data = self.data
        return Matrix3([
            data[0] * o.data[0] + data[1] * o.data[3] + data[2] * o.data[6],
            data[0] * o.data[1] + data[1] * o.data[4] + data[2] * o.data[7],
            data[0] * o.data[2] + data[1] * o.data[5] + data[2] * o.data[8],
            data[3] * o.data[0] + data[4] * o.data[3] + data[5] * o.data[6],
            data[3] * o.data[1] + data[4] * o.data[4] + data[5] * o.data[7],
            data[3] * o.data[2] + data[4] * o.data[5] + data[5] * o.data[8],
            data[6] * o.data[0] + data[7] * o.data[3] + data[8] * o.data[6],
            data[6] * o.data[1] + data[7] * o.data[4] + data[8] * o.data[7],
            data[6] * o.data[2] + data[7] * o.data[5] + data[8] * o.data[8]
        ])


class Matrix4:
    """
    Holds a transform matrix, consisting of a rotation matrix and a position. The has 12 element; it is assumed that
    the remaining four are (0, 0, 0, 1), producing a homogenous matrix.\

    :param data: holds the transform matrix data in array form
    """

    def __init__(self,
                 data: list[float] = None):
        if data is None:
            data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.data = data

    def __mul__(self, vector: Vector) -> Vector:
        """
        Transform the given vector by this matrix
        :param vector: The vector to transform
        :return: the transformed vector
        """
        data = self.data
        return Vector(
            vector.x * data[0] +
            vector.y * data[1] +
            vector.z * data[2] + data[3],
            vector.x * data[4] +
            vector.y * data[5] +
            vector.z * data[6] + data[7],
            vector.x * data[8] +
            vector.y * data[9] +
            vector.z * data[10] + data[11]
        )

    def __mul__(self, o: 'Matrix4') -> 'Matrix4':
        result = Matrix4()
        data = self.data
        result.data[0] = (o.data[0] * data[0]) + (o.data[4] * data[1]) + (o.data[8] * data[2])
        result.data[4] = (o.data[0] * data[4]) + (o.data[4] * data[5]) + (o.data[8] * data[6])
        result.data[8] = (o.data[0] * data[8]) + (o.data[4] * data[9]) + (o.data[8] * data[10])
        result.data[1] = (o.data[1] * data[0]) + (o.data[5] * data[1]) + (o.data[9] * data[2])
        result.data[5] = (o.data[1] * data[4]) + (o.data[5] * data[5]) + (o.data[9] * data[6])
        result.data[9] = (o.data[1] * data[8]) + (o.data[5] * data[9]) + (o.data[9] * data[10])
        result.data[2] = (o.data[2] * data[0]) + (o.data[6] * data[1]) + (o.data[10] * data[2])
        result.data[6] = (o.data[2] * data[4]) + (o.data[6] * data[5]) + (o.data[10] * data[6])
        result.data[10] = (o.data[2] * data[8]) + (o.data[6] * data[9]) + (o.data[10] * data[10])
        result.data[3] = (o.data[3] * data[0]) + (o.data[7] * data[1]) + (o.data[11] * data[2]) + data[3]
        result.data[7] = (o.data[3] * data[4]) + (o.data[7] * data[5]) + (o.data[11] * data[6]) + data[7]
        result.data[11] = (o.data[3] * data[8]) + (o.data[7] * data[9]) + (o.data[11] * data[10]) + data[11]
        return result
