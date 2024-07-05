import random

import cv2
import numpy as np

from core.particle import Particle
import application
from core.particle_force_generator import ParticleForceRegistry
from core.vector import Vector
from core.particle_force_generator import ParticleGravitationalForceGenerator


class MultiBodyGravitationSystemApplication(application.Application):

    def __init__(self, height: int, width: int, particles: list[Particle],
                 particle_force_registry: ParticleForceRegistry):
        self.duration = 1  # milliseconds
        super().__init__(width, height)
        self.particles = particles
        self.particle_force_registry = particle_force_registry

    def mouse_pressed(self, button: int, state: int, x: int, y: int):
        super().mouse_pressed(button, state, x, y)

    def key_pressed(self, key: int):
        super().key_pressed(key)

    def update(self):
        self.particle_force_registry.update_forces(self.duration)
        for particle in self.particles:
            particle.integrate(self.duration / 1000)
        # print([i.position.__str__() for i in self.particles])

    def display(self):
        img = np.zeros([self.height, self.width, 3])
        for particle in self.particles:
            x, y = int(particle.position.x), int(particle.position.y)
            cv2.circle(img, (x, y), 5, (255, 255, 255), -1)
        cv2.imshow(self.get_title(), img)

    def init_graphics(self):
        super().init_graphics()

    def get_title(self) -> str:
        return "Multi Body Gravity System"


if __name__ == "__main__":
    height = 1200
    width = 800
    particles = [
        Particle(
            position=Vector(100, 100),
            velocity=Vector(-100, -1000),
            acceleration=Vector.zero(),
            damping=0.9,
            inverse_mass=1,
        ),
        Particle(
            position=Vector(400, 600),
            velocity=Vector(100, 100),
            acceleration=Vector.zero(),
            damping=0.9,
            inverse_mass=1,
        ),
        # Particle(
        #     position=Vector(200, 600),
        #     velocity=Vector(100, -200),
        #     acceleration=Vector.zero(),
        #     damping=0.9,
        #     inverse_mass=1,
        # ),
        # Particle(
        #     position=Vector(20, 600),
        #     velocity=Vector(100, -200),
        #     acceleration=Vector.zero(),
        #     damping=0.9,
        #     inverse_mass=1,
        # ),
        # Particle(
        #     position=Vector(200, 60),
        #     velocity=Vector(-300, 300),
        #     acceleration=Vector.zero(),
        #     damping=0.9,
        #     inverse_mass=1,
        # ),
    ]
    particle_force_registry = ParticleForceRegistry()

    total_velocity = Vector.zero()
    for p in particles:
        p.position.z = 0
        p.velocity.z = 0
        total_velocity += p.velocity

    # particles.append(Particle(position=Vector(height/2, width/2), velocity=-total_velocity, damping=0.9))

    for i in particles:
        for j in particles:
            if i == j:
                continue
            fg = ParticleGravitationalForceGenerator(i, 10_000)
            particle_force_registry.add(j, fg)
    app = MultiBodyGravitationSystemApplication(height, width, particles, particle_force_registry)

    while True:
        app.update()
        app.display()
        if cv2.waitKey(1) == ord('q'):
            break
