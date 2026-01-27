# PlantMonitor

A comprehensive plant monitoring system with automated environmental control for optimal plant growth across different growth stages.

NOTE: This is currently in a state to be run on a local network only. Hardware used is a raspberry pi zero, a dht11 humidity/temperature sensor, and a kasa smart plug for controlling a fan.

## Features
- **Real-time Monitoring**: Temperature, humidity, and soil moisture tracking
- **Automated Fan Control**: Smart fan automation based on environmental thresholds
- **Growth Stage Management**: Customizable targets for Seedling, Vegetation, Flowering, and Late Flowering stages
- **Web Dashboard**: Interactive charts and real-time status display
- **Historical Data**: View sensor data over various time periods (60min to 7 days)
- **Manual Override**: Manual sensor updates and fan control when needed

## Hardware Requirements
- Raspberry Pi (or compatible single-board computer)
- DHT11 Temperature/Humidity sensor
- Kasa Smart Plug (for fan control)
- Fan or ventilation system
- Soil moisture sensor (optional)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/frigonj/PlantMonitor.git
   cd PlantMonitor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```


3. **Configure hardware:**
   - Connect DHT11 sensor to GPIO pin 4
   - Set up Kasa smart plug on your network
   - Update config.py with your smart plug IP address

4. **Initialize database:**
   ```bash 
   python -c "from database import db_utilities; db_utilities.init_db()"
   ```

## Configuration
Edit `config.py` to customize:

- **FAN_DEVICE_IP**: Your Kasa smart plug IP address
- **STATE_TARGETS**: Temperature/humidity ranges for each growth stage
- **Timing intervals**: Sensor check frequencies and automation settings

## Usage

### Development Mode (from venv)
```bash
source /venv/bin/activate
python app.py
```

### Production mode
```bash
nohup python -u app.py &
```

Access the web interface at `http://localhost:5000`

## Project Structure

```
PlantMonitor/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── controllers/              # Hardware controllers
│   └── fan_controller.py     # Kasa smart plug interface
├── automation/               # Automation logic
│   └── fan_automation.py     # Automated fan control
├── database/                 # Database utilities
│   └── db_utilities.py       # SQLite database operations
├── sensors/                  # Sensor modules
│   ├── sensor_readings.py    # DHT11 sensor interface
│   └── soil_moisture.py      # Soil moisture sensor
├── static/                   # Web assets (CSS, JS)
├── templates/                # HTML templates
└── scripts/                  # Utility scripts
```

## Automation Logic

### Fan Control 
- **Turn ON**: When temp/humidity exceeds maximum thresholds (with minimum safety buffer)
- **Turn OFF**: When readings drop 4° below max temp AND 4% below max humidity (with minimum safety buffer)
- **Check Frequency**: 30 seconds when fan is on, 5 minutes when off

### Growth Stages
Each stage has optimized temperature and humidity ranges:
- **Seedling**: 70-85°F, 70-80% humidity
- **Vegetation**: 70-85°F, 55-70% humidity
- **Flowering**: 65-80°F, 40-60% humidity
- **Late Flowering**: 65-80°F, 40-60% humidity

## API Endpoints
- `GET /` - Main dashboard
- `POST /set_state` - Change plant growth stage
- `GET /manual_update` - Trigger manual sensor reading
- `POST /fan/toggle` - Manual fan control
- `GET /api/history?range=24h` - Historical sensor data

## Dependencies
- Flask - Web framework
- python-kasa - Smart plug control
  - For kasa, you will also need cryptography and tzdata
- adafruit-dht - DHT11 sensor interface
- fasteners - File locking for sensor access
- sqlite3 - Database storage

## License
MIT License

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
