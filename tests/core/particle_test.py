import unittest
import random

from core.particle import Particle
from core.vector3 import Vector


class ParticleTest(unittest.TestCase):

    def test_simple_integrate(self):
        dt = 0.01

        for i in range(10):
            old_position = Vector.random() * random.randint(0, 100)
            old_velocity = Vector.random() * random.randint(0, 100)
            old_acceleration = Vector.random() * random.randint(0, 100)

            new_position = old_position + old_velocity * dt + old_acceleration * dt ** 2 * 0.5
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

    def test_clear_accumulator(self):
        position = Vector.random() * random.randint(0, 100)
        velocity = Vector.random() * random.randint(0, 100)
        acceleration = Vector.random() * random.randint(0, 100)

        particle = Particle(
            position=position,
            velocity=velocity,
            acceleration=acceleration,
            force_accum=Vector(random.random(), random.random(), random.random()),
        )
        particle.clear_accumulator()
        self.assertEqual(particle.force_accum, Vector.zero(),
                         msg=f'Particle force_accum should be {Vector.zero()}')

    def test_add_force(self):
        particle = Particle()
        forces = [Vector.random() for i in range(random.randint(4, 100))]
        for force in forces:
            particle.add_force(force)
        forces_sum = Vector.zero()
        for force in forces:
            forces_sum += force
        self.assertEqual(particle.force_accum, forces_sum,
                         msg=f'Particle force_accum should be {forces_sum}')
