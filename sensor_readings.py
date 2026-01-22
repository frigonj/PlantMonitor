import time
import board
import adafruit_dht

# Initialize DHT11 sensor on GPIO4 (physical pin 7)
dht = adafruit_dht.DHT11(board.D4)

print("DHT11 sensor test starting... Press CTRL+C to exit.")

for i in range (11):
    try:
        temperature_c = dht.temperature
        humidity = dht.humidity

        if temperature_c is not None and humidity is not None:
            temperature_f = (temperature_c * 9 / 5) + 32
            print(f"Temperature: {temperature_c:.1f}°F   Humidity: {humidity:.1f}%")
            i+=1
        else:
            print("Sensor returned None values")

    except RuntimeError as error:
        # DHT sensors often error — this is normal
        print("Retrying...", error)

    time.sleep(1)
