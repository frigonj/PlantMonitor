import sqlite3
import threading
from flask import Flask, render_template, request, redirect
import db_utilities as db
import sensor_readings as sens

app = Flask(__name__)

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
    print(f"SENSOR DATA: {sensor_data}")

    temp = sensor_data[2]
    temp = round(float(temp), 1)
    hum = sensor_data[3]
    hum = round(float(hum), 1)
    
    # # Example 'actual' readings (Replace with real sensor calls)
    actual = {"temp": temp, "hum": hum, "soil": 45} 
    
    # Evaluate Fan Logic [4]
    fan_needed = False
    # if actual['temp'] > targets['temp'][1]: # actual_temp > max_target_temp
    #     fan_needed = True
    # elif actual['hum'] > targets['hum'][1] and (actual['temp'] - targets['temp'][1] > 5):
    #     fan_needed = True

    return render_template('index.html', 
               state=current_state[0],
               actual=actual,
               targets=targets,
               temp_color=get_color(actual['temp'], targets['temp']),
               hum_color=get_color(actual['hum'], targets['hum']),
               soil_color=get_color(actual['soil'], targets['soil']),
               fan_status="ON" if fan_needed else "OFF")

@app.route('/set_state', methods=['POST'])
def set_state():
    db.update_plant_state(request.form['plant_state'])
    return redirect('/')

if __name__ == '__main__':
    db.init_db()
    db.get_reading()
    threading.Thread(target=sens.init_sens(), daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
    
    
