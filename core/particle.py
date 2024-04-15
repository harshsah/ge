from core.vector3 import Vector


class Particle:
    """
    A class to represent a particle. A particle is the simplest
    object that can be simulated in the system.

    :param position: Vector representing the position of the particle
    :type position: Vector

    :param velocity: Vector representing the velocity of the particle
    :type velocity: Vector

    :param acceleration: Vector representing the acceleration of the particle
    :type acceleration: Vector

    :param damping: The damping of the particle. Holds the amount of damping applied to linear motion. Damping is
    required to remove energy added through numerical instability in the integrator.
    :type damping: float

    :param inverse_mass: Holds the inverse of the mass of the particle. It is more useful to hold the inverse mass
    because integration is simpler and because in real-time simulation it is more useful to have objects with
    infinite mass (immovable) than zero mass (completely unstable in numerical simulation)
    :type inverse_mass: float

    :param: force_accum
    """

    def __init__(
            self,
            position: Vector = Vector.zero(),
            velocity: Vector = Vector.zero(),
            acceleration: Vector = Vector.zero(),
            damping: float = 1.0,
            inverse_mass: float = 0.0,
            force_accum: Vector = Vector.zero(),
    ):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.damping = damping
        self.inverse_mass = inverse_mass
        self.force_accum = force_accum

    def integrate(self, dt: float):
        """
        Integrates the particle forward in time by the given amount. This function uses a Newton-Euler integration
        method, which is a linear approximation of the correct integral. For this reason it may be inaccurate in some
        cases

        :param dt: The time step of the integration
        """

        # Update linear position
        # s2-s1 = u*t + a*t*t/2; ignoring second part as t*t is very small
        self.position += self.velocity * dt

        # resultant acceleration from the force
        result_acceleration = self.acceleration + self.force_accum * self.inverse_mass
        # Update linear velocity from the acceleration
        self.velocity += result_acceleration * dt
        # Impost drag
        self.velocity *= self.damping ** dt
