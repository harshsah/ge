from core.particle import Particle
from core.vector3 import Vector


class ParticleForceGenerator:
    """
    A force generator for adding one or more forces to particles
    """

    def update_force(self, particle: Particle, duration: float):
        """
        Calculates and updates the force applied to the given particle.
        :param particle: the particle whose force should be updated
        :param duration: the duration of the force applied
        :return:
        """
        pass


class ParticleGravity(ParticleForceGenerator):
    """
    A force generator that applies to gravity particles. One single instance can be used for multiple particles.

    :param gravity: holds acceleration due to gravity
    """

    def __init__(self, gravity: Vector = Vector.zero()):
        self.gravity = gravity

    def update_force(self, particle: Particle, duration: float):
        if particle.has_infinite_mass():
            return
        particle.add_force(self.gravity * particle.mass)


class ParticleDrag(ParticleForceGenerator):
    """
    A force generator that applies to drag particles. One instance can be used for multiple particles.

    :param k1: the velocity drag coefficient
    :param k2: the velocity squared drag coefficient
    """

    def __init__(self, k1: float = 0, k2: float = 0):
        self.k1 = k1
        self.k2 = k2

    def update_force(self, particle: Particle, duration: float):
        particle_velocity = particle.velocity
        particle_velocity_magnitude = particle_velocity.magnitude()
        force_magnitude = self.k1 * particle_velocity_magnitude + self.k2 * particle_velocity_magnitude ** 2
        force_direction = particle_velocity.normalize()
        force = force_magnitude * force_direction
        particle.add_force(-force)


class ParticleSpring(ParticleForceGenerator):
    """
    A force generator that applies a spring force.

    :param other: particle at the other end of the spring

    :param spring_constant: the spring constant

    :param rest_length: the length of the spring
    """

    def __init__(self, other: Particle, spring_constant: float, rest_length: float):
        self.other = other
        self.spring_constant = spring_constant
        self.rest_length = rest_length

    def update_force(self, particle: Particle, duration: float):
        position_a = particle.position
        position_b = self.other.position
        delta_position = position_a - position_b
        magnitude = delta_position.magnitude()
        delta_x = abs(magnitude - self.rest_length)
        force_direction = delta_position.normalize()
        force = -force_direction * delta_x * self.spring_constant
        particle.add_force(force)


class ParticleAnchoredSpring(ParticleForceGenerator):
    """
    A force generator that applies a spring force, where one end is attached ot a fixed point in space

    :param anchor: anchor position
    :param spring_constant: the spring constant
    :param rest_length: the length of the spring
    """

    def __init__(self, anchor: Vector, spring_constant: float, rest_length: float):
        self.anchor = anchor
        self.spring_constant = spring_constant
        self.rest_length = rest_length

    def update_force(self, particle: Particle, duration: float):
        delta_position = particle.position - self.anchor
        delta_position_magnitude = delta_position.magnitude()
        delta_x = abs(delta_position_magnitude - self.rest_length)
        force_direction = delta_position.normalize()
        force = - force_direction * delta_x * self.spring_constant
        particle.add_force(force)


class ParticleForceRegistration:
    """
    Keeps track of one force generator and the particle it applies to
    """

    def __init__(self, particle: Particle, particle_force_generator: ParticleForceGenerator):
        self.particle = particle
        self.particle_force_generator = particle_force_generator


class ParticleForceRegistry:
    """
    Holds all the force generators and the particle they apply to

    :param registry: the list of particle force generators
    """

    def __init__(self, registry: list[ParticleForceRegistration] = None):
        self.registry = registry or []

    def add(self, particle: Particle, particle_force_generator: ParticleForceGenerator):
        """
        Registers the given force generator to apply to the given particle.

        :param particle: the particle whose force should be registered
        :param particle_force_generator: the force generator to apply to the particle
        """
        pass

    def remove(self, particle: Particle, particle_force_generator: ParticleForceGenerator):
        """
        Removes the given registered pair from the registry. If the pair is not registered, this method will have no
        effect.

        :param particle: the particle whose force should be removed
        :param particle_force_generator: the force generator to remove from the particle

        """
        pass

    def clear(self):
        """
        Clears all registered force generators.
        """
        pass

    def update_forces(self, duration: float):
        """
        Calls all registered force generators to update the particle forces.
        :param duration: the duration of the force applied
        """

        for reg in self.registry:
            reg.particle_force_generator.update_force(reg.particle, duration)
