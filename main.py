import dearpygui.dearpygui as dpg
import sympy
import random
import tkinter as tk
import re


def _get_screen_size():
    root = tk.Tk()
    root.withdraw()
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.destroy()
    return width, height

# --- Regex Patterns, courtesy of AI ---
def _format_expression(expr):
    text = str(expr)
    replacements = [
        (r'-1\*([a-zA-Z0-9_]+)', r'-\1'),
        (r'-1\*\(([^()]+)\)', r'-(\1)'),
        (r'-1\*\[([^\]]+)\]', r'-[\1]'),
        (r'\b1\*\(([^()]+)\)', r'\1'),
        (r'\b1\*\[([^\]]+)\]', r'\1'),
        (r'\b1\*', ''),
        (r'\b(-?\d+)\*x\b', r'\1x'),
        (r'\(\s*(-?\d+)\s*([+\-])\s*(-?\d+)\s*\)', r'\1 \2 \3'),
        (r'\(\s*-\(?1\)?\s*\*\s*([^\)]+)\)', r'-\1'),
        (r'^\((-?[\d]+)\*\((.+)\)\)$', r'\1*(\2)'),
        (r'\(\((.+?)\)\)', r'(\1)')
    ]
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    if text.startswith('(') and text.endswith(')'):
        inner = text[1:-1]
        if inner.count('(') == inner.count(')'):
            text = inner
    return text

# --- Function to generate a random equation ---
def _generate_random_equation(x_symbol, solution, min_coefficient, max_coefficient, term_count, x_probability, shift_probability, inner_min, inner_max):
    terms = []
    for _ in range(term_count):
        use_x = random.randint(1, 100) <= x_probability
        outer_coefficient = random.randint(min_coefficient, max_coefficient)
        while outer_coefficient == 0:
            outer_coefficient = random.randint(min_coefficient, max_coefficient)
        inner_constant = random.randint(min_coefficient, max_coefficient)
        if use_x:
            x_coefficient = random.randint(inner_min, inner_max)
            while x_coefficient == 0:
                x_coefficient = random.randint(inner_min, inner_max)
            inner_expr = x_coefficient * x_symbol + inner_constant if random.choice([True, False]) else inner_constant - x_coefficient * x_symbol
        else:
            a = random.randint(min_coefficient, max_coefficient)
            b = random.randint(min_coefficient, max_coefficient)
            inner_expr = int(a + b) if random.choice([True, False]) else int(a - b)
        term = inner_expr if outer_coefficient == 1 else sympy.Mul(outer_coefficient, inner_expr, evaluate=False)
        terms.append(term)

    random.shuffle(terms)
    left_side_terms = []
    right_side_terms = []
    for term in terms:
        if random.randint(1, 100) <= shift_probability:
            right_side_terms.append(term)
        else:
            left_side_terms.append(term)
    if not left_side_terms:
        left_side_terms.append(right_side_terms.pop())
    if not right_side_terms:
        right_side_terms.append(left_side_terms.pop())
    left_expr = sympy.Add(*left_side_terms, evaluate=False)
    right_expr = sympy.Add(*right_side_terms, evaluate=False)
    left_value = left_expr.subs(x_symbol, solution)
    right_value = right_expr.subs(x_symbol, solution)
    correction = left_value - right_value
    right_expr = sympy.Add(right_expr, correction, evaluate=True)
    return left_expr, right_expr

# --- Function to generate and display the equation ---
def _generate_and_display_equation():
    min_coefficient = dpg.get_value("coef_min")
    max_coefficient = dpg.get_value("coef_max")
    min_solution = dpg.get_value("sol_min")
    max_solution = dpg.get_value("sol_max")
    min_operations = dpg.get_value("op_min")
    max_operations = dpg.get_value("op_max")
    x_probability = dpg.get_value("x_chance")
    shift_probability = dpg.get_value("rhs_chance")
    inner_min_coef = dpg.get_value("inner_coef_min")
    inner_max_coef = dpg.get_value("inner_coef_max")

    solution = random.randint(min_solution, max_solution)
    term_count = random.randint(min_operations, max_operations)
    x = sympy.symbols('x')
    left_side, right_side = _generate_random_equation(x, solution, min_coefficient, max_coefficient, term_count, x_probability, shift_probability, inner_min_coef, inner_max_coef)
    left_text = _format_expression(left_side)
    right_text = _format_expression(right_side)
    dpg.set_value("equation_text", f"{left_text} = {right_text}")
    dpg.set_item_user_data("show_solution_btn", solution)
    dpg.set_value("solution_text", "")

# --- Function to show the solution ---
def _show_equation_solution():
    solution = dpg.get_item_user_data("show_solution_btn")
    dpg.set_value("solution_text", f"x = {solution}")

# --- DearPyGui setup ---
screen_width, screen_height = _get_screen_size()
window_width, window_height = int(screen_width * 0.40), int(screen_height * 0.65)

dpg.create_context()
with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 4)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (80, 120, 255, 255))
dpg.bind_theme(global_theme)

with dpg.window(label="Equation Generator", tag="main_window", no_resize=True, no_title_bar=True, no_move=True):
    dpg.add_spacer(height=screen_height // 7)
    with dpg.group(horizontal=True):
        dpg.add_spacer(width=screen_width // 7)
        with dpg.group(horizontal=False):
            dpg.add_text("Equation Settings", bullet=True)
            dpg.add_spacer(height=5)
            dpg.add_text("Coefficient Range:")
            with dpg.group(horizontal=True):
                dpg.add_input_int(label="Min", tag="coef_min", default_value=-10, width=80)
                dpg.add_input_int(label="Max", tag="coef_max", default_value=10, width=80)
            dpg.add_spacer(height=5)
            dpg.add_text("Inner x coefficient range:")
            with dpg.group(horizontal=True):
                dpg.add_input_int(label="Min", tag="inner_coef_min", default_value=1, width=80)
                dpg.add_input_int(label="Max", tag="inner_coef_max", default_value=3, width=80)
            dpg.add_spacer(height=5)
            dpg.add_text("Solution Range:")
            with dpg.group(horizontal=True):
                dpg.add_input_int(label="Min", tag="sol_min", default_value=-10, width=80)
                dpg.add_input_int(label="Max", tag="sol_max", default_value=10, width=80)
            dpg.add_spacer(height=5)
            dpg.add_text("Number of Operations:")
            with dpg.group(horizontal=True):
                dpg.add_input_int(label="Min", tag="op_min", default_value=1, width=80)
                dpg.add_input_int(label="Max", tag="op_max", default_value=3, width=80)
            dpg.add_spacer(height=10)
            dpg.add_text("Term Distribution", bullet=True)
            dpg.add_spacer(height=5)
            dpg.add_text("Chance to include x in a term (%):")
            dpg.add_slider_int(tag="x_chance", default_value=70, min_value=0, max_value=100, width=200)
            dpg.add_text("Chance to shift a term to RHS (%):")
            dpg.add_slider_int(tag="rhs_chance", default_value=50, min_value=0, max_value=100, width=200)
            dpg.add_spacer(height=10)
            dpg.add_button(label="Generate Equation", callback=_generate_and_display_equation)
            dpg.add_spacer(height=15)
            with dpg.child_window(width=-1, height=40, border=False):
                dpg.add_text("", tag="equation_text")
            dpg.add_button(label="Show Solution", tag="show_solution_btn", callback=_show_equation_solution)
            dpg.add_text("", tag="solution_text")

dpg.create_viewport(title='Equation Generator', width=window_width, height=window_height)
dpg.set_viewport_resizable(False)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_item_pos("main_window", [0, 0])
dpg.set_item_width("main_window", window_width)
dpg.set_item_height("main_window", window_height)
dpg.start_dearpygui()
dpg.destroy_context()