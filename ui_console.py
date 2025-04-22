import pygame
import pygame_gui

def setup_ui(manager, window_width, window_height):
    panel_width = 300
    panel_rect = pygame.Rect(window_width - panel_width, 0, panel_width, window_height)

    panel = pygame_gui.elements.UIPanel(
        relative_rect=panel_rect,
        manager=manager,
        object_id="#console_panel"
    )

    # 50% opacity
    panel.background_colour = pygame.Color(0, 0, 0, 128)

    count_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(20, 20, 260, 25),
        text="Particle Count",
        manager=manager,
        container=panel
    )
    count_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(20, 50, 260, 25),
        start_value=100,
        value_range=(10, 1000),
        manager=manager,
        container=panel
    )

    size_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(20, 90, 260, 25),
        text="Particle Size",
        manager=manager,
        container=panel
    )
    size_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(20, 120, 260, 25),
        start_value=8,
        value_range=(2, 20),
        manager=manager,
        container=panel
    )

    spacing_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(20, 160, 260, 25),
        text="Spacing",
        manager=manager,
        container=panel
    )
    spacing_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(20, 190, 260, 25),
        start_value=20,
        value_range=(2, 60),
        manager=manager,
        container=panel
    )

    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(20, 230, 260, 40),
        text="Start Simulation",
        manager=manager,
        container=panel
    )

    return {
        'panel': panel,
        'count_slider': count_slider,
        'size_slider': size_slider,
        'spacing_slider': spacing_slider,
        'start_button': start_button,
        'sim_area_rect': pygame.Rect(0, 0, window_width - panel_width, window_height)
    }

def get_ui_values(ui_state):
    count = int(ui_state['count_slider'].get_current_value())
    size = int(ui_state['size_slider'].get_current_value())
    spacing = int(ui_state['spacing_slider'].get_current_value())
    return count, size, spacing
