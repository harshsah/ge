from core.particle import Particle
from core.vector3 import Vector


class ParticleContact:
    """
    A contact represents two object in contact  (in this case ParticleContact representing two particles). Resolving a
    contact removes their interpenetration, and applies sufficient impulse to keep them apart. Colliding bodies may also
    rebound.

    The contact has no callable functions, it just holds the contact details. To resolve a set of contacts, use the
    particle contact resolver class.

    :param paticle: the particles involved in the contact
    :param restitution: the coefficient of normal restitution at the contact
    :param contact_normal: the direction of the contact in the world coordinates
    """

    def __init__(self, particles: tuple[Particle], restitution: float, contact_normal: Vector):
        if len(particles) == 0:
            raise ValueError("Particles cannot be empty")
        if len(particles) >= 2:
            raise ValueError("Particles cannot contain more than two particles")
        self.particles = particles
        self.restitution = restitution
        self.contact_normal = contact_normal

    def resolve(self, duration: float):
        """
        Resolves this contact, for both velocity and interpenetration
        :param duration: the duration
        """
        self._resolve_velocity(duration)

    def _calculate_separating_velocity(self) -> float:
        """
        Calculates the separating velocity of the contact
        :return: the separating velocity of the contact
        """
        particle_a = self.particles[0]
        particle_b = self.particles[1]
        relative_velocity = particle_a.velocity
        if particle_b is not None:
            relative_velocity -= particle_b.velocity
        return relative_velocity.scaler_product(self.contact_normal)

    def _resolve_velocity(self, duration: float):
        """
        Handles the impulse calculations for this collision.
        :param duration: the duration
        """
        pass
