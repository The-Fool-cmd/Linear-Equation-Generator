import numpy as np
import pygame

# Hardcoded constants
PRESSURE_CONSTANT = 500000.0  # Reduced gas constant to decrease pressure forces
CUBIC_SPLINE_CONSTANT = 10.0 # Adjusted constant for cubic spline kernel
DRAG = 0.995 # Drag coefficient for velocity damping

class SmoothingKernel:
    """
    UNSTABLE AS FUCK, DO NOT USE THESE
    @staticmethod
    def poly6(dst, radius):
        if dst >= radius:
            return 0.0
        factor = 315 / (64 * np.pi * radius ** 9)
        return factor * (radius ** 2 - dst ** 2) ** 3
    
    @staticmethod
    def spiky_gradient(r_vec, radius):
        dst = np.linalg.norm(r_vec)
        if dst == 0 or dst >= radius:
            return np.zeros(2)
        factor = -45 / (np.pi * radius ** 6)
        return factor * (radius - dst) ** 2 * (r_vec / dst)

    @staticmethod
    def viscosity_laplacian(dst, radius):
        if dst >= radius:
            return 0.0
        factor = 45 / (np.pi * radius ** 6)
        return factor * (radius - dst)
    """
    @staticmethod
    def cubic_spline(dst, radius):
        value = max(0.0, radius ** 2 - dst ** 2)
        return value ** 3 / CUBIC_VOLUME * CUBIC_SPLINE_CONSTANT

    @staticmethod
    def cubic_spline_gradient(r_vec, radius):
        dst = np.linalg.norm(r_vec)
        if dst >= radius or dst < 1e-8:  # Avoid division by zero
            return np.zeros(2)
        factor = -6 * (radius ** 2 - dst ** 2) ** 2 / CUBIC_VOLUME
        return factor * (r_vec / dst)

    @staticmethod
    def cubic_spline_laplacian(dst, radius):
        if dst >= radius:
            return 0.0
        factor = -12 * (radius ** 2 - dst ** 2) / CUBIC_VOLUME
        return factor * (radius ** 2 - 3 * dst ** 2)


# works well atm
def update_density(particles, h):
    for i, pi in enumerate(particles):
        density = 0.0
        for j, pj in enumerate(particles):
            r_vec = pi.pos - pj.pos
            dst = np.linalg.norm(r_vec)
            if dst >= h:
                continue
            dst = np.linalg.norm(r_vec)
            density += SmoothingKernel.cubic_spline(dst, h)
        pi.density = density



def update_pressure(particles):
    for p in particles:
        p.pressure = max(0, PRESSURE_CONSTANT * (p.density - REST_DENSITY))

def update_pressure_force(particles, radius):
    for i, pi in enumerate(particles):
        force_pressure = np.zeros(2)
        for j, pj in enumerate(particles):
            if pi is pj:
                continue
            r_vec = pi.pos - pj.pos
            dst = np.linalg.norm(r_vec)
            if dst < radius and dst > 0 and pj.density > 1e-5:
                grad_w = SmoothingKernel.cubic_spline_gradient(r_vec, radius)
                force_pressure += -0.5 * (pi.pressure + pj.pressure) / pj.density * grad_w
        pi.force = force_pressure

def update_viscosity_force(particles, radius):
    for i, pi in enumerate(particles):
        force_viscosity = np.zeros(2)
        for j, pj in enumerate(particles):
            if pi is pj:
                continue
            r_vec = pi.pos - pj.pos
            dst = np.linalg.norm(r_vec)
            if dst < radius and dst > 0:
                lap_w = SmoothingKernel.cubic_spline_laplacian(dst, radius)
                force_viscosity += lap_w * (pj.vel - pi.vel) / pj.density
        pi.force += force_viscosity

class Particle:
    def __init__(self, x, y, radius=10):
        self.pos = np.array([x, y], dtype=np.float32)
        self.vel = np.zeros(2, dtype=np.float32)
        self.force = np.zeros(2, dtype=np.float32)
        self.density = 0.0
        self.pressure = 0.0
        self.radius = radius

    def update(self, bounds, dt):
        self.vel += self.force * dt / self.density  # mass = 1
        # print(self.density)
        self.vel *= DRAG  # Apply drag to the velocity
        self.pos += self.vel

        w, h = bounds
        if self.pos[0] - self.radius < 0:
            self.pos[0] = self.radius  # Prevent sticking to the left border
            self.vel[0] *= -1
        elif self.pos[0] + self.radius > w:
            self.pos[0] = w - self.radius  # Prevent sticking to the right border
            self.vel[0] *= -1

        if self.pos[1] - self.radius < 0:
            self.pos[1] = self.radius  # Prevent sticking to the top border
            self.vel[1] *= -1
        elif self.pos[1] + self.radius > h:
            self.pos[1] = h - self.radius  # Prevent sticking to the bottom border
            self.vel[1] *= -1

    def draw(self, surface):
        # Map density to a color gradient from red (low density) to blue (high density)
        max_density = REST_DENSITY * 2  # Use twice the rest density as the upper bound
        min_density = REST_DENSITY * 0.5  # Use half the rest density as the lower bound
        normalized_density = (self.density - min_density) / (max_density - min_density)
        normalized_density = max(0.0, min(1.0, normalized_density))  # Clamp between 0 and 1
        red = int((1 - normalized_density) * 255)
        blue = int(normalized_density * 255)
        color = (red, 0, blue)
        pygame.draw.circle(surface, color, self.pos.astype(int), self.radius)

class ParticleSystem:
    def __init__(self, count, radius, spacing, width, height):
        global SMOOTHING_LENGTH, CUBIC_VOLUME, REST_DENSITY
        # Adjust smoothing length based on simulation box dimensions and particle count
        particle_spacing = (width * height / count) ** 0.5
        SMOOTHING_LENGTH = particle_spacing * 2.0  # tune as needed

        CUBIC_VOLUME = np.pi * SMOOTHING_LENGTH ** 8 / 4.0
        W0 = (SMOOTHING_LENGTH ** 2) ** 3 / CUBIC_VOLUME
        REST_DENSITY = 20.0 * W0  # tune as needed

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
                self.particles.append(Particle(x, y, radius=radius))

    def apply_random_kick(self):
        if not self.kick_applied:
            for p in self.particles:
                p.vel = np.random.uniform(-1.5, 1.5, size=2)
            self.kick_applied = True

    def update(self, time_delta):
        # Step 1: Density estimation
        update_density(self.particles, self.h)
        # Step 2: Pressure calculation
        update_pressure(self.particles)
        # Step 3: Pressure force calculation
        update_pressure_force(self.particles, self.h)
        # Step 4: Viscosity force calculation
        update_viscosity_force(self.particles, self.h)
        # Step 5: Integration
        for p in self.particles:
            p.update(self.bounds, time_delta)

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)
