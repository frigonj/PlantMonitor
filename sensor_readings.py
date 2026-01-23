import time
import board
import adafruit_dht
import db_utilities as db
import soil_moisture as sm

# Initialize DHT11 sensor on GPIO4 (physical pin 7)
dht = adafruit_dht.DHT11(board.D4)



def init_sens():
    print("Pulling Initial sensor Readings...", flush=True)
    temperatures = []
    humidities = []
    for i in range (11):
        print(f"Percent complete: {i/11}%", flush=True)
        try:
            temperature_c = dht.temperature
            humidity = dht.humidity
            if temperature_c is not None and humidity is not None:
                temperature_f = (temperature_c * 9 / 5) + 32
                temperatures.append(temperature_f)
                humidities.append(humidity)
                i+=1
        except: 
            pass
        time.sleep(.1)
    avg_temp = sum(temperatures) / len(temperatures)
    avg_hum = sum(humidities) / len(humidities)
    db.add_reading(avg_temp, avg_hum, 55)
    print(f"Average Temperatures: {avg_temp:.1f}°F  Average Humidity {avg_hum}%")

def get_temp_hum(): 
    print("Pulling sensor Readings...")
    temperatures = []
    humidities = []
    for i in range (11):
        print(f"Percent complete: {i/11}%")       
        try:
            temperature_c = dht.temperature
            humidity = dht.humidity
            if temperature_c is not None and humidity is not None:
                temperature_f = (temperature_c * 9 / 5) + 32
                temperatures.append(temperature_f)
                humidities.append(humidity) 
                i+=1
        except:
            pass
        time.sleep(.1)

    avg_temp = sum(temperatures) / len(temperatures)
    avg_hum = sum(humidities) / len(humidities)
    db.add_reading(avg_temp, avg_hum, 55)
    print(f"Average Temperatures: {avg_temp:.1f}°F  Average Humidity {avg_hum}%")
    return {"temperature":avg_temp, "humidity":avg_hum}

# TODO: Add in soil moisture to this.

