from core.particle import Particle
from core.vector3 import Vector


class ParticleContact:
    """
    A contact represents two object in contact  (in this case ParticleContact representing two particles). Resolving a
    contact removes their interpenetration, and applies sufficient impulse to keep them apart. Colliding bodies may also
    rebound.

    The contact has no callable functions, it just holds the contact details. To resolve a set of contacts, use the
    particle contact resolver class.

    :param particles: the particles involved in the contact
    :param restitution: the coefficient of normal restitution at the contact
    :param contact_normal: the direction of the contact in the world coordinates
    :param penetration: the depth of penetration at the contact
    """

    def __init__(
            self,
            particles: tuple[Particle],
            restitution: float,
            contact_normal: Vector,
            penetration: float,
    ):
        if len(particles) == 0:
            raise ValueError("Particles cannot be empty")
        if len(particles) >= 2:
            raise ValueError("Particles cannot contain more than two particles")
        if len(particles) == 1:
            particles = particles[0], None
        self.particles = particles
        self.restitution = restitution
        self.contact_normal = contact_normal
        self.penetration = penetration

    def resolve(self, duration: float):
        """
        Resolves this contact, for both velocity and interpenetration
        :param duration: the duration
        """
        self._resolve_velocity(duration)

    def calculate_separating_velocity(self) -> float:
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

        # Find the velocity in the direction of the contact.
        separating_velocity = self.calculate_separating_velocity()

        # Check whether it needs to be resolved.
        if separating_velocity > 0:
            # The contact is either separating or stationary - there’s no impulse required.
            return

        # Calculate the new separating velocity.
        new_sep_velocity = -separating_velocity * self.restitution
        delta_velocity = new_sep_velocity - separating_velocity

        # We apply the change in velocity to each object in proportion to its inverse mass
        # (i.e., those with lower inverse mass [higher actual mass] get less change in velocity).
        total_inverse_mass = self.particles[0].inverse_mass
        if self.particles[1]:
            total_inverse_mass += self.particles[1].inverse_mass

        # If all particles have infinite mass, then impulses have no effect.
        if total_inverse_mass <= 0:
            return

        # Calculate the impulse to apply.
        impulse = delta_velocity / total_inverse_mass

        # Find the amount of impulse per unit of inverse mass.
        impulse_per_inverse_mass = self.contact_normal * impulse

        # Apply impulses: they are applied in the direction of the contact,
        # and are proportional to the inverse mass.
        self.particles[0].velocity += impulse_per_inverse_mass * self.particles[0].inverse_mass

        if self.particles[1]:
            # Particle 1 goes in the opposite direction.
            self.particles[1].velocity += impulse_per_inverse_mass * -self.particles[1].inverse_mass

    def resolve_interpenetration(self):
        """
        Handles the interpenetration resolution for this contact
        """
        # If we don't have any penetration, skip this step
        if self.penetration <= 0:
            return

        # The movement of each object is based on its inverse mass, so total that
        total_inverse_mass = self.particles[0].inverse_mass
        if self.particles[1]:
            total_inverse_mass += self.particles[1].inverse_mass

        # If all particles have infinite mass, then we do nothing
        if total_inverse_mass <= 0:
            return

        # Find the amount of penetration resolution per unit of inverse mass
        move_per_inverse_mass = self.contact_normal * (-self.penetration) / total_inverse_mass

        # Apply the penetration resolution
        self.particles[0].position += move_per_inverse_mass * self.particles[0].inverse_mass
        if self.particles[1]:
            self.particles[1].position += move_per_inverse_mass * self.particles[1].inverse_mass


class ParticleContactResolver:
    """
    The contact resolution routine for particle contacts. One resolver instance can be shared for the whole simulation.

    :param iterations: holds the number of iterations allowed
    """

    def __init__(self,iterations: int):
        """
        Creates a new contact resolver
        :param iterations: holds the number of iterations allowed
        """
        self.iterations = iterations
        self.iterations_used = 0

    def resolve_contacts(self, contact_list: list[ParticleContact], duration: float):
        """
        Resolves a set of particle contacts for both penetration and velocity

        :param contact_list: the list of particle contacts
        :param duration: the duration passed
        """
        self.iterations_used = 0
        while self.iterations_used < self.iterations:
            # Find the contact with the largest closing velocity
            max_velocity = 0
            num_contacts = len(contact_list)
            max_index = num_contacts
            for i in range(num_contacts):
                separation_velocity = contact_list[i].calculate_separating_velocity()
                if separation_velocity < max_velocity:
                    max_velocity = separation_velocity
                    max_index = i
            contact_list[max_index].resolve(duration)
            self.iterations_used += 1
