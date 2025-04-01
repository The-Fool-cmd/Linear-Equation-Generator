#!/bin/bash
sudo apt-get update && sudo apt-get install -y python3-tk && sudo apt install python3.12-venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python3 main.py &
