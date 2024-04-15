import unittest
import random

from core.particle import Particle
from core.vector3 import Vector


class ParticleTest(unittest.TestCase):

    def test_simple_integrate(self):
        dt = 0.01

        for i in range(10):

            old_position = Vector(random.random(), random.random(), random.random()) * random.randint(0, 100)
            old_velocity = Vector(random.random(), random.random(), random.random()) * random.randint(0, 100)
            old_acceleration = Vector(random.random(), random.random(), random.random()) * random.randint(0, 100)

            new_position = old_position + old_velocity * dt + old_acceleration * dt**2 * 0.5
            new_velocity = old_velocity + old_acceleration * dt

            particle = Particle(
                position=old_position,
                velocity=old_velocity,
                acceleration=old_acceleration,
            )
            particle.integrate(dt)

            self.assertEqual(particle.position, new_position,
                             f'Particle position should be {new_position}, but {particle.position}')
            self.assertEqual(particle.velocity, new_velocity,
                             f'Particle velocity should be {new_velocity}, but {particle.velocity}')
