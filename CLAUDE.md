# PlantMonitor

## Commands

```bash
# Release (Windows — merges develop -> main, pushes)
bash scripts/release.sh

# Deploy (run on Pi via SSH after release)
~/PlantMonitor/scripts/deploy.sh
```

## Stack

- Python 3, Flask (dev server — intentional, not production)
- SQLite3 via db_utilities.py
- python-kasa (async) for Kasa smart plug control
- adafruit-dht for DHT11 sensor on GPIO pin 4
- fasteners for cross-process file locking (/tmp/sensor.lock)
- Bootstrap 5 + Chart.js dashboard (templates/index.html, static/js/dashboard.js)

## Deployment Environment

All code runs on a remote Raspberry Pi (192.168.50.12, user: admin, hostname: plantmonitor). There is no local runtime environment for this project.

- Never run pip, python, ssh, or app-level commands directly — the user must run them on the Pi via SSH.
- When a change requires a Pi-side action (deploy, restart, package install), state the exact command for the user to run rather than running it yourself.
- Deploy workflow: Windows side runs `bash scripts/release.sh`, then user SSHes to Pi and runs `~/PlantMonitor/scripts/deploy.sh`.

## Conventions

- Config (IPs, thresholds, ports) lives in config.py — never hardcode elsewhere.
- All GPIO access must go through the fasteners lock at /tmp/sensor.lock with acquire(timeout=10).
- Timestamps stored as UTC (datetime.utcnow()); dashboard JS appends ' UTC' when constructing Date objects.
- Fan control is humidity-only — temperature is handled by a separate heater, not the fan.

## Architecture Notes

- app.py — Flask entry point, routes, template rendering
- automation/fan_automation.py — background daemon thread, humidity-based fan control loop
- controllers/fan_controller.py — async python-kasa wrapper with retry logic
- database/db_utilities.py — SQLite CRUD (readings + settings key-value tables)
- sensors/sensor_readings.py — DHT11 averaging (10 samples), C->F conversion
- Pi venv at /home/admin/PlantMonitor/venv/; DB at /home/admin/db/plant_monitor.db
