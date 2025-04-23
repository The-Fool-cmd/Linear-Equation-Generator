import pygame
import pygame_gui
from simulation import ParticleSystem
from ui_console import setup_ui, get_ui_values
"""
import cProfile
import pstats
import io
"""

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("SPH Prototype")
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
ui_state = setup_ui(manager, WINDOW_WIDTH, WINDOW_HEIGHT)

count, size, spacing = get_ui_values(ui_state)
particles = ParticleSystem(count, size, spacing, WINDOW_WIDTH - 300, WINDOW_HEIGHT)
particles.count = count
particles.size = size
particles.spacing = spacing

running = True
simulation_started = False
fps_update_timer = 0  # Add this at the top of the file

# Initialize fps_text with a default value before the main loop
fps_text = pygame.font.SysFont("consolas", 16).render("FPS: 0", True, (255, 255, 255))

while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == ui_state['start_button']:
                    particles.apply_random_kick()
                    simulation_started = True
                    print("Simulation started")
                elif event.ui_element == ui_state['apply_button']:
                    count, size, spacing = get_ui_values(ui_state)
                    particles = ParticleSystem(count, size, spacing, WINDOW_WIDTH - 300, WINDOW_HEIGHT)

        manager.process_events(event)

    manager.update(time_delta)
    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (50, 50, 50), ui_state['sim_area_rect'], width=2)

    if simulation_started:
        particles.update(time_delta)
    particles.draw(screen)

    font = pygame.font.SysFont("consolas", 16)
    fps_update_timer += time_delta
    if fps_update_timer >= 1.0:  # Update FPS text every second
        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
        fps_update_timer = 0
    
    manager.draw_ui(screen)
    screen.blit(fps_text, (WINDOW_WIDTH - 90, 10))
    pygame.display.flip()

pygame.quit()
