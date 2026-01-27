FAN_DEVICE_IP = "192.168.50.11"
STATE_TARGETS = {
    "Seedling": {"temp": (70, 85), "hum": (70, 80), "soil": (65, 70)},
    "Vegetation": {"temp": (70, 85), "hum": (55, 70), "soil": (40, 70)},
    "Flowering": {"temp": (65, 80), "hum": (40, 60), "soil": (40, 50)},
    "Late Flowering": {"temp": (65, 80), "hum": (40, 60), "soil": (30, 40)}
}

# Flask Configuration
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000

####The following has not yet been implemented: ####
# Sensor Configuration
#SENSOR_SAMPLES = 10
#SENSOR_SAMPLE_DELAY = 0.2
#DHT_GPIO_PIN = 4

# Automation Timing
#FAN_ON_CHECK_INTERVAL = 30    # seconds
#FAN_OFF_CHECK_INTERVAL = 300  # seconds

# Fan Control Thresholds
#FAN_TEMP_BUFFER = 4  # degrees below max to turn off
#FAN_HUM_BUFFER = 4   # percent below max to turn off
#FAN_MIN_BUFFER = 2   # buffer above minimum before turning on/off