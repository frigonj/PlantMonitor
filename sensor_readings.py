import time
import board
import adafruit_dht

# Initialize DHT11 sensor on GPIO4 (physical pin 7)
dht = adafruit_dht.DHT11(board.D4)

print("DHT11 sensor test starting... Press CTRL+C to exit.")

while True:
    try:
        temperature_c = dht.temperature
        humidity = dht.humidity

        if temperature_c is not None and humidity is not None:
            print(f"Temperature: {temperature_c:.1f}°C   Humidity: {humidity:.1f}%")
        else:
            print("Sensor returned None values")

    except RuntimeError as error:
        # DHT sensors often error — this is normal
        print("Retrying...", error)

    time.sleep(2)
