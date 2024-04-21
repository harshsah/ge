from core.particle import Particle
from core.vector3 import Vector


class ParticleContact:
    """
    A contact represents two object in contact  (in this case ParticleContact representing two particles). Resolving a
    contact removes their interpenetration, and applies sufficient impulse to keep them apart. Colliding bodies may also
    rebound.

    The contact has no callable functions, it just holds the contact details. To resolve a set of contacts, use the
    particle contact resolver class.

    :param particle_a: the first particle involved in the contact.
    :param particle_b: the second particle involved in the contact. It can be None for contacts with the scenery
    :param restitution: the coefficient of normal restitution at the contact
    :param contact_normal: the direction of the contact in the world coordinates
    """

    def __init__(self, particle_a: Particle, particle_b: Particle, restitution: float, contact_normal: Vector):
        self.particle_a = particle_a
        self.particle_b = particle_b
        self.restitution = restitution
        self.contact_normal = contact_normal

    def resolve(self, duration: float):
        self._resolve_velocity(duration)

    def _calculate_separating_velocity(self) -> float:
        relative_velocity = self.particle_a.velocity
        if self.particle_b is not None:
            relative_velocity -= self.particle_b.velocity
        return relative_velocity.scaler_product(self.contact_normal)

    def _resolve_velocity(self, duration: float):
        pass
