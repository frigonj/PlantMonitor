import sqlite3
from flask import Flask, render_template, request, redirect
import database_manager as db # Using the tools we created earlier


app = Flask(__name__)

# Target mapping based on sources [1-3]
STATE_TARGETS = {
    "Seedling": {
        "temp": (70, 85), "hum": (70, 80), "soil": (65, 70)
    },
    "Vegetation": {
        "temp": (70, 85), "hum": (55, 70), "soil": (40, 70)
    },
    "Flowering": {
        "temp": (65, 80), "hum": (40, 60), "soil": (40, 50)
    },
    "Late Flowering": {
        "temp": (65, 80), "hum": (40, 60), "soil": (30, 40)
    }
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
    targets = STATE_TARGETS[current_state]
    
    # Example 'actual' readings (Replace with real sensor calls)
    actual = {"temp": 78, "hum": 65, "soil": 45} 
    
    # Evaluate Fan Logic [4]
    fan_needed = False
    if actual['temp'] > targets['temp'][1]: # actual_temp > max_target_temp
        fan_needed = True
    elif actual['hum'] > targets['hum'][1] and (actual['temp'] - targets['temp'][1] > 5):
        fan_needed = True

    return render_template('index.html', 
               state=current_state,
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

DB_FILE = "plant_monitor.db"

def init_db():
    """Initializes the database schema."""
    with sqlite3.connect(DB_FILE) as conn:
        # Table for historical readings
        conn.execute('''CREATE TABLE IF NOT EXISTS readings 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         timestamp DATETIME, 
                         temp REAL, 
                         humidity REAL, 
                         soil_moisture REAL)''')
        
        # Table for persistent app settings (e.g., current Plant State)
        conn.execute('''CREATE TABLE IF NOT EXISTS settings 
                        (key TEXT PRIMARY KEY, value TEXT)''')
        
        # Default state: Seedling [1]
        conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('plant_state', 'Seedling')")
        conn.commit()

if __name__ == '__main__':
    db.init_db()
    app.run(host='0.0.0.0', port=5000)
