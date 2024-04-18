import numpy as np

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


class ParticleGravityForceGenerator(ParticleForceGenerator):
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


class ParticleDragForceGenerator(ParticleForceGenerator):
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


class ParticleSpringForceGenerator(ParticleForceGenerator):
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


class ParticleAnchoredSpringForceGenerator(ParticleForceGenerator):
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
        delta_x = delta_position_magnitude - self.rest_length
        print(delta_x)
        force_direction = delta_position.normalize()
        force = - force_direction * delta_x * self.spring_constant
        particle.add_force(force)


class ParticleBungeeForceGenerator(ParticleForceGenerator):
    """
    A force generator that applies a spring force only when extended.

    :param other: particle at the other end of the spring

    :param spring_constant: the spring constant

    :param rest_length: the length of the bungee string
    """

    def __init__(self, other: Particle, spring_constant: float, rest_length: float):
        self.other = other
        self.spring_constant = spring_constant
        self.rest_length = rest_length

    def update_force(self, particle: Particle, duration: float):
        delta_position = particle.position - self.other.position
        delta_position_magnitude = delta_position.magnitude()

        # Check if bungee is compressed
        if delta_position_magnitude <= self.rest_length:
            return

        force_direction = delta_position.normalize()
        force = force_direction * self.spring_constant * delta_position_magnitude
        particle.add_force(-force)


class ParticleAnchoredBungeeForceGenerator(ParticleForceGenerator):
    """
    A force generator that applies a spring force, where one end is attached ot a fixed point in space.
    applies a spring force only when extended

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
        delta_x = delta_position_magnitude - self.rest_length
        # print(delta_x)
        if delta_x < 0:
            return
        force_direction = delta_position.normalize()
        force = - force_direction * delta_x * self.spring_constant
        # print(force, force.magnitude())
        particle.add_force(force)


class ParticleBuoyancyForceGenerator(ParticleForceGenerator):
    """
    A force generator that applies a buoyancy force for a plane of liquid parallel to XZ plane.

    Archimedes' principle is the statement that the buoyant force on an object is equal to the weight of the fluid
    displaced by the object

    :param max_depth: property of the particle. the maximum submersion depth of the object before it generates its maximum buoyancy force
    :param volume: property of the particle. the volume of the object
    :param water_height: property of liquid body. the height of the water plane above y=0. The plane will be parallel to the XZ plane
    :param liquid_density: property of liquid body. The density of the liquid
    :param gravity: property of the world. The gravity acceleration in the world
    """

    def __init__(self, max_depth: float, volume: float, water_height: float, liquid_density: float, gravity: float):
        self.max_depth = max_depth
        self.volume = volume
        self.water_height = water_height
        self.liquid_density = liquid_density
        self.gravity = gravity

    def update_force(self, particle: Particle, duration: float):

        # Check if particle is out of the water
        if particle.position.y >= self.water_height + self.max_depth:
            return

        # Check if the particle is at max depth
        if particle.position.y <= self.water_height - self.max_depth:
            force = Vector(y=self.liquid_density * self.volume)
            particle.add_force(force)
        # Check if the particle is partly submerged
        else:
            # This might be incorrect
            fraction_submerged = (-particle.position.y + self.max_depth + self.water_height) / self.max_depth
            force = Vector(y=self.liquid_density * fraction_submerged * self.volume * self.gravity)
            particle.add_force(force)


class ParticleGravitationalForceGenerator(ParticleForceGenerator):
    """
    Calculates and updates force due to gravitation among particle following Newton's Law

    :param other: other particle that will generate the gravitational field
    :param gravitational_constant: the gravitational constant
    """

    def __init__(self, other: Particle, gravitational_constant: float):
        self.other = other
        self.gravitational_constant = gravitational_constant

    def update_force(self, particle: Particle, duration: float):
        delta_x = particle.position - self.other.position
        force_direction = delta_x.normalize()
        delta_x_magnitude = force_direction.magnitude()

        force_magnitude = self.gravitational_constant * self.other.mass * particle.mass / (delta_x_magnitude ** 2)
        force = force_direction * force_magnitude
        particle.add_force(-force)


class ParticleFakeSpringForceGenerator(ParticleForceGenerator):
    """
    A force generator that fakes a stiff spring force, and where one end is attached to a fixed point in space.

    :param anchor: position of anchored end of the spring

    :param spring_constant: the spring constant

    :param damping: the damping on the oscillation of the spring
    """

    def __init__(self, anchor: Vector, spring_constant: float, damping: float):
        self.anchor = anchor
        self.spring_constant = spring_constant
        self.damping = damping

    def update_force(self, particle: Particle, duration: float):
        if particle.has_infinite_mass():
            return

        # relive position of the particle to the anchor
        position = particle.position - self.anchor

        # calculate the constants and check whether they are in bounds
        gamma = 0.5 * (4 * self.spring_constant - self.damping ** 2) ** 0.5

        if gamma == 0:
            return

        c = position * self.damping / 2 / gamma + particle.velocity / gamma

        # calculate target position
        target = position * np.cos(gamma * duration) + c * np.sin(gamma * duration)
        target *= np.exp(-0.5 * duration * self.damping)

        # calculate the resulting acceleration and force
        acceleration = (target - position) / (duration ** 2) - particle.velocity * duration
        particle.add_force(acceleration * particle.mass)


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
        self.registry.append(ParticleForceRegistration(particle, particle_force_generator))

    def remove(self, particle: Particle, particle_force_generator: ParticleForceGenerator):
        """
        Removes the given registered pair from the registry. If the pair is not registered, this method will have no
        effect.

        :param particle: the particle whose force should be removed
        :param particle_force_generator: the force generator to remove from the particle

        """
        temp = []
        for i in range(len(self.registry)):
            if self.registry[i].particle == particle and self.registry[
                i].particle_force_generator == particle_force_generator:
                temp.append(i)

        self.registry = temp

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
