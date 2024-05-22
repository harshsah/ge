from core.particle import Particle
from core.particle_contact import ParticleContact


class ParticleLink:
    """
    Links connect two particles together, generating a contact if they violate the constraints of the link. It is used
    as a base class for cables and rods, and could be used as a base class for springs with a limit to their externsion.

    :param particles: holds the pair of particles that are connected by this link
    """

    def __init__(self, particles: tuple[Particle, Particle]):
        """
        :param particles: holds the pair of particles that are connected by this link
        """
        self.particles = particles

    def _current_length(self):
        """
        :return: the current length of the cable
        """
        pass

    def fill_contact(self, contact: ParticleContact, limit: float) -> int:
        """
        Fills the given contact structure wth the contact needed to keep th link from violating its constraint. The
        contact pointer should point to the first available contact in a contact in a contact array, where limit is the
        maximum number of contacts in the array that can be written to. The method returns the number of contacts that
        have been written. This format is common to contact-generating functions, but this class can only generate a
        single contact, so the pointer can be pointer to a single element.

        :param contact:
        :param limit: limit parameter is assumed to be at least one (zero isn't valid).
        :return: either 0, if the cable wasn't overextended, or one if a contact was needed
        """
        return 0


class ParticleCable(ParticleLink):
    """
    Cables link a pair of particles, generating a contact if they stray too far apart.
    """

    def __init__(self, particles: tuple[Particle, Particle], max_length: float, restitution: float):
        """
        :param particles: holds the pair of particles that are connected by this link
        :param max_length: hold the maximum length of the cable
        :param restitution: holds the restitution of the cable
        """
        super().__init__(particles)
        self.max_length = max_length
        self.restitution = restitution

    def _current_length(self):
        particle_a, particle_b = self.particles
        relative_position = particle_a.position - particle_b.position
        return relative_position.magnitude()

    def fill_contact(self, contact: ParticleContact, limit: float) -> int:

        # Length of the cable
        length = self._current_length()

        # Check if overextended
        if length < self.max_length:
            return 0

        # else return the contact
        particle_a, particle_b = self.particles
        contact.particles = self.particles

        # Calculate the normal
        normal = particle_b.position - particle_a.position
        normal.normalize()
        contact.contact_normal = normal

        contact.penetration = length - self.max_length
        contact.restitution = self.restitution

        return 1


class ParticleRod(ParticleLink):
    """
     Rods link a pair of particles, generating a contact if they stray too far apart or too close.
    """

    def __init__(self, length: float, particles: tuple[Particle, Particle]):
        """
        :param length: holds the length of the rod
        :param particles: holds the pair of particles that are connected by this link
        """
        super().__init__(particles)
        self.length = length

    def _current_length(self):
        particle_a, particle_b = self.particles
        relative_position = particle_a.position - particle_b.position
        return relative_position.magnitude()

    def fill_contact(self, contact: ParticleContact, limit: float) -> int:

        # Find the length of the rod
        current_length = self._current_length()

        # Check if we are overextended
        if current_length == self.length:
            return 0

        # else return the contact
        contact.particles = self.particles
        particle_a, particle_b = self.particles

        # Calculate the normal
        normal = particle_b.position - particle_a.position
        normal.normalize()

        # The contact normal depends on whether we're extending or compressing
        if current_length > self.length:
            contact.contact_normal = normal
            contact.penetration = current_length - self.length
        else:
            contact.contact_normal = -normal
            contact.penetration = self.length - current_length

        # always use zero restitution (no bounciness)
        contact.restitution = 0

        return 1


