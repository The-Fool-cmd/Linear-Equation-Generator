import numpy as np
import pygame

# Hardcoded constants
SMOOTHING_LENGTH = 20.0
REST_DENSITY = 1.0
GAS_CONSTANT = 200.0

class SmoothingKernel:
    @staticmethod
    def poly6(r, h):
        if r >= h:
            return 0.0
        factor = 315 / (64 * np.pi * h ** 9)
        return factor * (h ** 2 - r ** 2) ** 3

    @staticmethod
    def spiky_gradient(r_vec, h):
        r = np.linalg.norm(r_vec)
        if r == 0 or r >= h:
            return np.zeros(2)
        factor = -45 / (np.pi * h ** 6)
        return factor * (h - r) ** 2 * (r_vec / r)

    @staticmethod
    def viscosity_laplacian(r, h):
        if r >= h:
            return 0.0
        factor = 45 / (np.pi * h ** 6)
        return factor * (h - r)

class Particle:
    def __init__(self, x, y, radius=10):
        self.pos = np.array([x, y], dtype=np.float32)
        self.vel = np.zeros(2, dtype=np.float32)
        self.force = np.zeros(2, dtype=np.float32)
        self.density = 0.0
        self.pressure = 0.0
        self.radius = radius

    def update(self, bounds):
        self.vel += self.force  # mass = 1
        self.pos += self.vel

        w, h = bounds
        if self.pos[0] - self.radius < 0 or self.pos[0] + self.radius > w:
            self.vel[0] *= -1
        if self.pos[1] - self.radius < 0 or self.pos[1] + self.radius > h:
            self.vel[1] *= -1

    def draw(self, surface):
        # Use hue for density
        color_intensity = min(255, int(self.density * 255))
        color = (0, color_intensity, 255)
        pygame.draw.circle(surface, color, self.pos.astype(int), self.radius)

class ParticleSystem:
    def __init__(self, count, size, spacing, width, height):
        self.particles = []
        self.bounds = (width, height)
        self.h = SMOOTHING_LENGTH
        self.kick_applied = False

        # Place particles in a center-out square grid
        grid_w = int(np.sqrt(count))
        start_x = width // 2 - (grid_w // 2) * spacing
        start_y = height // 2 - (grid_w // 2) * spacing

        for i in range(count):
            row = i // grid_w
            col = i % grid_w
            x = start_x + col * spacing
            y = start_y + row * spacing
            if x < width and y < height:
                self.particles.append(Particle(x, y, radius=size))

    def apply_random_kick(self):
        if not self.kick_applied:
            for p in self.particles:
                p.vel = np.random.uniform(-1.5, 1.5, size=2)
            self.kick_applied = True

    def update(self):
        # Step 1: Density estimation
        for i, pi in enumerate(self.particles):
            density = 0.0
            for j, pj in enumerate(self.particles):
                r_vec = pi.pos - pj.pos
                r = np.linalg.norm(r_vec)
                density += SmoothingKernel.poly6(r, self.h)
            pi.density = density

        # Step 2: Pressure calculation
        for p in self.particles:
            p.pressure = GAS_CONSTANT * (p.density - REST_DENSITY)

        # Step 3: Pressure force calculation
        for i, pi in enumerate(self.particles):
            force_pressure = np.zeros(2)
            for j, pj in enumerate(self.particles):
                if i == j:
                    continue
                r_vec = pi.pos - pj.pos
                r = np.linalg.norm(r_vec)
                if r < self.h and r > 0:
                    grad_w = SmoothingKernel.spiky_gradient(r_vec, self.h)
                    force_pressure += -0.5 * (pi.pressure + pj.pressure) / pj.density * grad_w
            pi.force = force_pressure

        # Step 4: Integration
        for p in self.particles:
            p.update(self.bounds)

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)
