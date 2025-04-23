import pygame
import pygame_gui

def setup_ui(manager, window_width, window_height):
    panel_width = 300
    panel_rect = pygame.Rect(window_width - panel_width, 0, panel_width, window_height)

    # Add a flag to avoid unnecessary UI updates
    ui_update_needed = False

    panel = pygame_gui.elements.UIPanel(
        relative_rect=panel_rect,
        starting_layer_height=1,
        manager=manager,
        object_id="#console_panel"
    )

    panel.background_colour = pygame.Color(0, 0, 0, 128)

    count_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(20, 20, 260, 25),
        text="Particle Count",
        manager=manager,
        container=panel
    )
    count_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(20, 50, 260, 25),
        manager=manager,
        container=panel
    )
    count_input.set_text("50")

    size_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(20, 90, 260, 25),
        text="Particle Size",
        manager=manager,
        container=panel
    )
    size_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(20, 120, 260, 25),
        manager=manager,
        container=panel
    )
    size_input.set_text("10")

    spacing_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(20, 160, 260, 25),
        text="Spacing",
        manager=manager,
        container=panel
    )
    spacing_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(20, 190, 260, 25),
        manager=manager,
        container=panel
    )
    spacing_input.set_text("20")

    apply_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(20, 230, 260, 40),
        text="Apply Settings",
        manager=manager,
        container=panel
    )

    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(20, 280, 260, 40),
        text="Start Simulation",
        manager=manager,
        container=panel
    )

    return {
        'panel': panel,
        'count_input': count_input,
        'size_input': size_input,
        'spacing_input': spacing_input,
        'apply_button': apply_button,
        'start_button': start_button,
        'sim_area_rect': pygame.Rect(0, 0, window_width - panel_width, window_height),
        'last_values': (100, 8, 20), # Default values
        'ui_update_needed': ui_update_needed  # Include the flag in the returned dictionary
    }

def get_ui_values(ui_state):
    try:
        count = int(ui_state['count_input'].get_text())
    except ValueError:
        count = ui_state['last_values'][0]
    try:
        size = int(ui_state['size_input'].get_text())
    except ValueError:
        size = ui_state['last_values'][1]
    try:
        spacing = int(ui_state['spacing_input'].get_text())
    except ValueError:
        spacing = ui_state['last_values'][2]

    # Only update UI values if they have changed
    if (count, size, spacing) != ui_state['last_values']:
        ui_state['ui_update_needed'] = True
    else:
        ui_state['ui_update_needed'] = False

    ui_state['last_values'] = (count, size, spacing)
    return count, size, spacing
