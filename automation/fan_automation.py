import threading
import time
import fasteners
import config
from database import db_utilities as db
from sensors import sensor_readings as sens
from controllers import fan_controller as fan


class FanAutomation:
    def __init__(self, device_ip):
        self.device_ip = device_ip
        self.running = False
        self.thread = None
        self.lock = fasteners.InterProcessLock('/tmp/sensor.lock')

    def control_loop(self):
        while self.running:
            try:
                if self.lock.acquire(timeout=10):
                    try:
                        sens.init_sens()
                    finally:
                        self.lock.release()
                else:
                    print("Fan automation: could not acquire sensor lock within 10s, skipping cycle.")
                    time.sleep(30)
                    continue

                current_state = db.get_current_state()
                sensor_data = db.get_reading()
                if not current_state or not sensor_data:
                    print("Fan automation: no state or sensor data yet, skipping cycle.")
                    time.sleep(30)
                    continue

                hum = float(sensor_data[3])
                hum_min, hum_max = config.STATE_TARGETS[current_state[0]]["hum"]

                try:
                    fan_status = fan.get_fan_status(self.device_ip)
                except Exception:
                    fan_status = True  # assume on if we can't reach the plug

                if not fan_status and hum > hum_max:
                    print(f"Fan ON - humidity {hum}% exceeds max {hum_max}%")
                    fan.turn_fan_on(self.device_ip)
                elif fan_status and hum < hum_min:
                    print(f"Fan OFF - humidity {hum}% below min {hum_min}%")
                    fan.turn_fan_off(self.device_ip)
                else:
                    print(f"Fan unchanged - humidity {hum}% (target {hum_min}-{hum_max}%, fan={'on' if fan_status else 'off'})")

            except Exception as e:
                print(f"Fan automation error: {e}")

            try:
                current_fan_status = fan.get_fan_status(self.device_ip)
                sleep_time = 30 if current_fan_status else 300
            except Exception:
                sleep_time = 30

            time.sleep(sleep_time)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.control_loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False


automation = None

def start_automation(device_ip):
    global automation
    if automation is None:
        automation = FanAutomation(device_ip)
        automation.start()

def stop_automation():
    global automation
    if automation:
        automation.stop()
        automation = None
