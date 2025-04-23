import pygame
import pygame_gui

from simulation import ParticleSystem
from ui_console import setup_ui, handle_ui_events, get_ui_values

# Init Pygame
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("SPH Prototype")
clock = pygame.time.Clock()

# UI
manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
ui_state = setup_ui(manager, WINDOW_WIDTH, WINDOW_HEIGHT)

# Initial particle system preview
initial_count, initial_size, initial_spacing = get_ui_values(ui_state)
particles = ParticleSystem(initial_count, initial_size, initial_spacing, WINDOW_WIDTH - 300, WINDOW_HEIGHT)

# State
running = True
simulation_started = False

while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        handle_ui_events(event, manager, ui_state)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == ui_state['start_button']:
                    simulation_started = True
                    particles.apply_random_kick()
            elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if not simulation_started:
                    count, size, spacing = get_ui_values(ui_state)
                    particles = ParticleSystem(count, size, spacing, WINDOW_WIDTH - 300, WINDOW_HEIGHT)

        manager.process_events(event)

    manager.update(time_delta)
    screen.fill((0, 0, 0))

    # Draw simulation area border
    pygame.draw.rect(screen, (50, 50, 50), ui_state['sim_area_rect'], width=2)

    # Draw particles
    if simulation_started:
        particles.update()
    particles.draw(screen)

    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
