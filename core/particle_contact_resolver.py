from core.particle_contact import ParticleContact


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


