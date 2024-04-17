import cv2
import numpy as np

import application
from core.particle import Particle
from core.particle_force_generator import ParticleForceRegistry, ParticleSpringForceGenerator, \
    ParticleAnchoredSpringForceGenerator
from core.vector3 import Vector


class ParticleSpringSystemApplication(application.Application):

    def __init__(self, particle: Particle, particle_force_registry: ParticleForceRegistry, anchor: Vector):
        super().__init__(600, 800)
        self.duration = 10 # millis
        self.particle = particle
        self.anchor = anchor
        self.particle_force_registry = particle_force_registry

    def get_title(self) -> str:
        return "Particle Spring System"

    def init_graphics(self):
        super().init_graphics()

    def display(self):
        img = np.zeros([self.height, self.width, 3], dtype=np.uint8)
        particle_position = (int(self.particle.position.x), int(self.particle.position.y))
        anchor_position = (int(self.anchor.x), int(self.anchor.y))
        cv2.circle(img, particle_position, 5, (255, 255, 255), -1)
        cv2.circle(img, anchor_position, 5, (0, 0, 255), -1)
        cv2.line(img, anchor_position, particle_position, (0, 255, 0), 1)
        cv2.imshow(self.get_title(), img)

    def update(self):
        self.particle_force_registry.update_forces(self.duration)
        self.particle.integrate(self.duration / 1000)

    def key_pressed(self, key: int):
        super().key_pressed(key)

    def mouse_pressed(self, button: int, state: int, x: int, y: int):
        super().mouse_pressed(button, state, x, y)



if __name__ == "__main__":
    particle =  Particle(
            position=Vector(400, 350),
            velocity=Vector(0, 0),
            acceleration=Vector(y=10),
            damping=0.99,
            inverse_mass=0.01,
        )
    anchor = Vector(400, 100)

    particle_force_registry = ParticleForceRegistry()
    fg = ParticleAnchoredSpringForceGenerator(anchor, 10, 200)
    particle_force_registry.add(particle, fg)

    app = ParticleSpringSystemApplication(particle, particle_force_registry, anchor)

    while True:
        app.display()
        app.update()
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


