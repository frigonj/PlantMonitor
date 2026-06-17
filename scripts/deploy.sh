#!/bin/bash
# Run on the Pi after `git pull` to apply the latest changes.
set -e

REPO_DIR="/home/admin/PlantMonitor"
SERVICE="plant-monitor"

cd "$REPO_DIR"

git pull

# Sync Python dependencies if requirements.txt changed
if git diff HEAD@{1} HEAD --name-only 2>/dev/null | grep -q "requirements.txt"; then
    echo "requirements.txt changed -- updating dependencies..."
    venv/bin/pip install -r requirements.txt -q
fi

sudo systemctl restart "$SERVICE"
sudo systemctl status "$SERVICE" --no-pager -l
