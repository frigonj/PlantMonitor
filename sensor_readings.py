#!/home/admin/PlantMonitor/venv/bin/python3

import time
import board
import adafruit_dht
import db_utilities as db
import soil_moisture as sm

# Initialize DHT11 sensor on GPIO4 (physical pin 7)
dht = adafruit_dht.DHT11(board.D4)

def init_sens():
    print("Pulling sensor Readings...", flush=True)
    temperatures = []
    humidities = []
    target_samples = 10
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
        print(f"Average Temperatures: {avg_temp:.1f}°F  Average Humidity {avg_hum}%")
    finally: 
        dht.exit()

# TODO: Add in soil moisture to this.

