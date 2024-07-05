from core.particle import Particle
from core.particle_contact import ParticleContact, ParticleContactResolver, ParticleContactGenerator
from core.particle_force_generator import ParticleForceRegistry


class ParticleWorld:
    """
    Keeps track of a set of particles, an provides the mens to update them all
    """

    def __init__(self, max_contacts: int, iterations: int):
        """
        Creates a new particle simulator that can handle up to the given number of contacts per frame. You can also
        optionally give a number of contact-resolution iterations to use. If you don't give a number of iterations,then
        twice the number of contacts will be used
        :param max_contacts:
        :return:
        """
        self.particles: list[Particle] = []
        self.contacts = []
        self.max_contacts = max_contacts
        self.iterations = iterations
        self.calculater_iterations = (iterations == 0)
        self.registry: ParticleForceRegistry = ParticleForceRegistry()
        self.resolver: ParticleContactResolver = ParticleContactResolver(10)
        self.contact_gen: list[ParticleContactGenerator] = []

    def start_frame(self):
        """
        Initializes the world for a simulation frame. This clears the force accumulators for particles in the for the
        particles in the world. After calling this,the particles can have their forces for the frame added.
        """
        for particle in self.particles:
            particle.clear_accumulator()

    def generate_contacts(self) -> int:
        """
        Calls each of the registered contact generators to report their contacts. Returns the number of generator
        contacts.

        :return: The number of generated contacts
        """
        limit = self.max_contacts
        contact_i = 0
        for g in self.contact_gen:
            next_contact = self.contacts[contact_i]
            used = g.add_contact(next_contact, limit)
            limit -= used
            contact_i += used

            # we have run out of contacts to fill. This means we're missing contacts.
            if limit <= 0:
                break

        # Return the number of contacts used;
        return self.max_contacts - limit

    def integrate(self, duration: float):
        """
        Integrate all the particles in the world forward in time by the given duration.

        :param duration: the duration
        """
        for particle in self.particles:
            # remove all forces from the accumulator
            particle.integrate(duration)

    def run_physics(self, duration: float):
        """
        processes all the physics for the particle world
        :param duration: the duration
        """
        # first apply the force generators
        self.registry.update_forces(duration)

        # then integrate the objects
        self.integrate(duration)

        # generate contacts
        used_contacts = self.generate_contacts()

        # add process them
        if self.calculater_iterations:
            self.resolver.iterations = used_contacts * 2
        self.resolver.resolve_contacts(self.contacts, used_contacts, duration)

