#!/bin/bash
set -e  # stop on error

echo "Updating packages and installing venv module..."
sudo apt-get update
sudo apt-get install -y python3-venv

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install pygame==2.6.1 pygame_gui==0.6.3 numpy

echo "Running main.py..."
python3 main.py