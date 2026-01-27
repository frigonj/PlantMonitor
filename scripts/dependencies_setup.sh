#!/bin/bash
#TODO: Generate a new dependencies file

# 1. Update system packages
sudo apt update && sudo apt upgrade -y

# 2. Install Python 3, Pip, and SQLite3 CLI
sudo apt install python3 python3-pip python3-venv sqlite3 -y

# install git
sudo apt install git -y

#install micro text editor
sudo apt install micro

# 3. Create project directory and move into it
mkdir /plant_monitor
cd /plant_monitor

# 4. Create a virtual environment to keep dependencies organized
python3 -m venv venv
source venv/bin/activate

# 5. Install Flask
pip install Flask
pip install tzone

# 6. Create standard Flask directory structure
mkdir static templates
mkdir static/css static/js

# 7. Download Bootstrap (Local Copy)
# Since you want this offline/local, we download Bootstrap files directly
wget https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css -P static/css/
wget https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.css -P static/js/

echo "Installation complete. Your project is ready in /plant_monitor"