#!/home/admin/PlantMonitor/venv/bin/python3

import time
import board
import adafruit_dht
import db_utilities as db
import soil_moisture as sm
from datetime import datetime, timedelta

# Initialize DHT11 sensor on GPIO4 (physical pin 7)
def safe_init_dht():
    while True:
        try:
            dht = adafruit_dht.DHT11(board.D4)
            return dht
        except RuntimeError as e:
            print("Failed to initialize DHT, retrying:", e)
            time.sleep(2)

def init_sens():
    print("Init Sens...", flush=True)
    temperatures = []
    humidities = []
    target_samples = 10
    dht = safe_init_dht()
    try:
        while len(temperatures) < target_samples:
            try:
                temperature_c = dht.temperature
                humidity = dht.humidity
                if temperature_c is not None and humidity is not None:
                    temperature_f = (temperature_c * 9 / 5) + 32
                    temperatures.append(temperature_f)
                    humidities.append(humidity)
                    percent=(len(temperatures)/target_samples*100)
                    print(f"Percent complete: {percent:.1f}%", end="\r", flush=True)
            except: 
                pass
            time.sleep(.2)
        avg_temp = sum(temperatures) / len(temperatures)
        avg_hum = sum(humidities) / len(humidities)
        db.add_reading(avg_temp, avg_hum, 55)
        print(f"{datetime.now().strftime("%B %d, %Y %I:%M:%S %p")}: Temperature: {avg_temp:.1f}°F  Humidity: {avg_hum}%")
    finally: 
        dht.exit()

# TODO: Add in soil moisture to this.

