#!/home/admin/PlantMonitor/venv/bin/python3

import sqlite3
import threading
import db_utilities as db
import sensor_readings as sens
import fasteners
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, jsonify, request

lock = fasteners.InterProcessLock('/tmp/sensor.lock')

app = Flask(__name__)

# Fan device IP - update this with your actual device IP
FAN_DEVICE_IP = "192.168.50.11"  # Replace with your smart plug IP

# Target mapping based on sources [1-3]
STATE_TARGETS = {
    "Seedling": { "temp": (70, 85), "hum": (70, 80), "soil": (65, 70)},
    "Vegetation": { "temp": (70, 85), "hum": (55, 70), "soil": (40, 70)},
    "Flowering": { "temp": (65, 80), "hum": (40, 60), "soil": (40, 50)},
    "Late Flowering": { "temp": (65, 80), "hum": (40, 60), "soil": (30, 40)}
}

def get_color(val, target_range):
    """Logic: Green = target, Yellow = +/- 2, Red = outside [3]."""
    t_min, t_max = target_range
    if t_min <= val <= t_max:
        return "success" # Green
    elif (t_min - 2) <= val <= (t_max + 2):
        return "warning" # Yellow
    else:
        return "danger"  # Red

@app.route('/')
def index():
    current_state = db.get_current_state()
    targets = STATE_TARGETS[current_state[0]]
    sensor_data = db.get_reading()
    print(repr(sensor_data[1]))
    dt = datetime.strptime(sensor_data[1], "%Y-%m-%d %H:%M:%S.%f")
    time = dt.strftime("%m/%d/%Y %I:%M:%S %p")
    temp = sensor_data[2]
    temp = round(float(temp), 1)
    hum = sensor_data[3]
    hum = round(float(hum), 1)
    
    # # Example 'actual' readings (Replace with real sensor calls)
    actual = {"time": time, "temp": temp, "hum": hum, "soil": 45} 
    
    try:
        fan_status = fan.get_fan_status(FAN_DEVICE_IP)
        fan_status_text = "ON" if fan_status else "OFF"
    except:
        fan_status_text = "ERROR"
    

    return render_template('index.html', 
               state=current_state[0],
               actual=actual,
               targets=targets,
               temp_color=get_color(actual['temp'], targets['temp']),
               hum_color=get_color(actual['hum'], targets['hum']),
               soil_color=get_color(actual['soil'], targets['soil']),
               fan_status=fan_status_text)

@app.route('/set_state', methods=['POST'])
def set_state():
    db.update_plant_state(request.form['plant_state'])
    return redirect('/')

@app.route("/manual_update")
def manual_update():
    with lock:
            sens.init_sens()
    return redirect("/")

@app.route('/fan/toggle', methods=['POST'])
def toggle_fan():
    try:
        current_status = fan.get_fan_status(FAN_DEVICE_IP)
        if current_status:
            fan.turn_fan_off(FAN_DEVICE_IP)
        else:
            fan.turn_fan_on(FAN_DEVICE_IP)
    except Exception as e:
        print(f"Fan control error: {e}")
    return redirect('/')

@app.route("/api/history")
def history():
    range_map = {
        "60m": 60,
        "6h": 360,
        "12h": 720,
        "24h": 1440,
        "7d": 10080
    }

    period = request.args.get("range", "24h")
    minutes = range_map.get(period, 1440)

    rows = db.get_readings_range(minutes)

    timestamps = []
    temps = []
    hums = []
    soils = []

    for row in rows:
        timestamps.append(row["timestamp"])
        temps.append(row["temp"])
        hums.append(row["hum"])
        soils.append(row["soil_moisture"])

    return jsonify({
        "timestamps": timestamps,
        "temperature": temps,
        "humidity": hums,
        "soil": soils
    })

if __name__ == '__main__':
    db.init_db()
    db.get_reading()
    app.run(host='0.0.0.0', port=5000)