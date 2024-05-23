from core.particle import Particle


class ParticleWorld:
    """
    Keeps track of a set of particles, an provides the mens to update them all
    """

    def __int__(self, particles: list[Particle]):
        """
        Creates a new particle simulator that can handle up to the given number of contacts per frame. You can also
        optionally give a number of contact-resolution iterations to use. If you don't give a number of iterations,then
        twice the number of contacts will be used
        :param particles:
        :return:
        """
        self.particles = particles

