#!/bin/bash
set -e  # stop on error
echo "Activating virtual environment..."
source venv/bin/activate

echo "Running main.py..."
python3 main.py