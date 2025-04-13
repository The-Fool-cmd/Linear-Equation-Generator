# Linear Equation Generator

A simple yet powerful Python GUI app to generate linear equations with customizable structure and difficulty.

Built with [Dear PyGui](https://github.com/hoffstadt/dearpygui) and [SymPy](https://www.sympy.org/), this tool lets you:

- Generate linear equations of the form `ax + b = cx + d`
- Customize coefficient ranges, number of operations, and solution constraints
- Include or exclude terms with `x`
- Shift terms across both sides of the equation
- Visually display and copy equations with a friendly GUI
- Reveal the solution on demand

---

## 📦 Requirements

- Python 3.8+
Installed using the setup files provided:
- [dearpygui](https://pypi.org/project/dearpygui/)
- [sympy](https://pypi.org/project/sympy/)
- **Linux only:** `python3-tk` for screen resolution detection

## 🚀 Quick Start

### 🪟 Windows

```bash
./setup_windows.bat
```

### 🐧 Linux/macOS

```bash
chmod +x setup_linux.sh
./setup_linux.sh
```

These scripts will:
1. Install `python3-tk` (Linux only)
2. Create a virtual environment
3. Install dependencies from `requirements.txt`
4. Launch the app

---

## 🧮 Features

| Feature                    | Description |
|---------------------------|-------------|
| Coefficient Range         | Set min/max for term constants |
| Number of Operations      | Choose how many additive/multiplicative terms appear |
| Solution Range            | Limit the range of valid `x` values |
| Include `x` in Terms      | Set a percent chance that terms include `x` |
| RHS Term Shifting         | Randomly shift terms to the right-hand side |
| Equation Preview          | View and copy the generated equation |
| Solution Reveal           | Display the solution on demand |

---

## 📂 File Structure

```
├── main.py                # Main application script
├── requirements.txt       # Python dependencies
├── setup_windows.bat      # One-click setup for Windows
├── setup_linux.sh         # One-click setup for Linux/macOS
```

---

## 🛠 Future Ideas

- Export equations as images and copy to clipboard
- Step by step solutions
- Math quiz generator mode with scoring and adjustable difficulty

---

## 🧑‍💻 Author

Created by The Fool, with AI assistance.  
Feel free to fork, share, or contribute!
