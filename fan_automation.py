import threading
import time
import db_utilities as db
import sensor_readings as sens
import fan_controller as fan
import fasteners

class FanAutomation:
    def __init__(self, device_ip):
        self.device_ip = device_ip
        self.running = False
        self.thread = None
        self.lock = fasteners.InterProcessLock('/tmp/sensor.lock')
        
        self.STATE_TARGETS = {
            "Seedling": {"temp": (70, 85), "hum": (70, 80)},
            "Vegetation": {"temp": (70, 85), "hum": (55, 70)},
            "Flowering": {"temp": (65, 80), "hum": (40, 60)},
            "Late Flowering": {"temp": (65, 80), "hum": (40, 60)}
        }
    
    def should_turn_on_fan(self, temp, hum, targets):
        return temp > targets["temp"][1] or hum > targets["hum"][1]
    
    def should_turn_off_fan(self, temp, hum, targets):
        temp_ok = temp <= (targets["temp"][1] - 4) and temp >= (targets["temp"][0] + 2)
        hum_ok = hum <= (targets["hum"][1] - 4) and hum >= (targets["hum"][0] + 2)
        return temp_ok and hum_ok
    
    def control_loop(self):
        while self.running:
            try:
                with self.lock:
                    sens.init_sens()
                
                current_state = db.get_current_state()
                sensor_data = db.get_reading()
                temp = float(sensor_data[2])
                hum = float(sensor_data[3])
                targets = self.STATE_TARGETS[current_state[0]]
                
                try:
                    fan_status = fan.get_fan_status(self.device_ip)
                except:
                    fan_status = True  # Assume fan is on if error getting status                
                if not fan_status and self.should_turn_on_fan(temp, hum, targets):
                    fan.turn_fan_on(self.device_ip)
                    print(f"Fan ON - Temp: {temp}°F, Hum: {hum}%")
                elif fan_status and self.should_turn_off_fan(temp, hum, targets):
                    fan.turn_fan_off(self.device_ip)
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
