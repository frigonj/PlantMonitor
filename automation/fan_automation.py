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
        self.fan_on_reason = None # "temp" or "hum" or None
        self.lock = fasteners.InterProcessLock('/tmp/sensor.lock')
    
    def should_turn_on_fan(self, temp, hum, targets):
        temp_exceeds_max = temp > targets["temp"][1]
        hum_exceeds_max = hum > targets["hum"][1]
        temp_above_min = temp >= (targets["temp"][0])
        hum_above_min = hum >= (targets["hum"][0])
        print(f"CHECK FAN_ON: T={temp}°F (max={targets['temp'][1]}, min={targets['temp'][0]}) H={hum}% (max={targets['hum'][1]}, min={targets['hum'][0]}) | T_exceeds={temp_exceeds_max} H_exceeds={hum_exceeds_max} T_above_min={temp_above_min} H_above_min={hum_above_min}")
        if temp_exceeds_max and hum_above_min:
            return "temp"
        if hum_exceeds_max and temp_above_min:
            self.fan_on_reason = "hum"
        return None
    
    def should_turn_off_fan(self, temp, hum, targets):
        temp_in_range = temp <= targets["temp"][1] and temp >= targets["temp"][0]
        hum_in_range = hum <= targets["hum"][1] and hum >= targets["hum"][0]
        temp_below_min = temp < targets["temp"][0]
        hum_below_min = hum < targets["hum"][0]
        print(f"CHECK FAN_OFF: T={temp}°F H={hum}% | reason={self.fan_on_reason} T_in_range={temp_in_range} H_in_range={hum_in_range} T_below_min={temp_below_min} H_below_min={hum_below_min}")
        if self.fan_on_reason == "temp":
            return temp_in_range or hum_below_min
        if self.fan_on_reason == "hum":
            return hum_in_range or temp_below_min
        return True
    
    def control_loop(self):
        while self.running:
            try:
                with self.lock:
                    sens.init_sens()
                current_state = db.get_current_state()
                sensor_data = db.get_reading()
                temp = float(sensor_data[2])
                hum = float(sensor_data[3])
                targets = config.STATE_TARGETS[current_state[0]]
                try:
                    fan_status = fan.get_fan_status(self.device_ip)
                except:
                    fan_status = True  # Assume fan is on if error getting status                
                if not fan_status:
                    reason = self.should_turn_on_fan(temp, hum, targets)
                    if reason:
                        print(f"Turning on fan due to {reason} threshold breach.")
                        self.fan_on_reason = reason
                        fan.turn_fan_on(self.device_ip)
                        print(f"Fan ON ({reason}) - Temp: {temp}°F, Hum: {hum}%")
                elif fan_status and self.should_turn_off_fan(temp, hum, targets):
                    print("Turning off fan - conditions back in range.")
                    fan.turn_fan_off(self.device_ip)
                    self.fan_on_reason = None
                    print(f"Fan OFF - Temp: {temp}°F, Hum: {hum}%")
            except Exception as e:
                print(f"Fan automation error: {e}")

            # Dynamic sleep based on fan status
            try:
                current_fan_status = fan.get_fan_status(self.device_ip)
                sleep_time = 30 if current_fan_status else 300  # 30sec if on, 5 min if off
            except:
                sleep_time = 30  # Default to 30 sec if can't get status
            
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
