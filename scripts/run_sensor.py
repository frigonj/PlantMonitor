#!/home/admin/PlantMonitor/venv/bin/python3

import sensors.sensor_readings as sens
import fasteners

lock = fasteners.InterProcessLock('/tmp/sensor.lock')

if __name__ == "__main__":
    with lock:
            sens.init_sens()
