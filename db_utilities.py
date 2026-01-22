import sqlite3
from datetime import datetime, timedelta

DB_FILE = "../db/plant_monitor.db"

def init_db():
    """Initializes the database schema."""
    with sqlite3.connect(DB_FILE) as conn:
        # Table for historical readings
        conn.execute('''CREATE TABLE IF NOT EXISTS readings 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         timestamp DATETIME, 
                         temp REAL, 
                         hum REAL, 
                         soil_moisture REAL)''')
        
        # Table for persistent app settings (e.g., current Plant State)
        conn.execute('''CREATE TABLE IF NOT EXISTS settings 
                        (key TEXT PRIMARY KEY, value TEXT)''')
        
        # Default state: Seedling [1]
        conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('plant_state', 'Seedling')")
        conn.commit()

def update_plant_state(new_state):
    """Updates the persistent plant state in the database."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("UPDATE settings SET value = ? WHERE key = 'plant_state'", (new_state,))
        conn.commit()

def get_current_state():
    """Retrieves the saved plant state."""
    with sqlite3.connect(DB_FILE) as conn:
        result = conn.execute("SELECT value FROM settings WHERE key = 'plant_state'").fetchone()
        return result if result else "No Result was found"

def add_reading(temp, hum, soil_moisture):
    """Logs new sensor data with a timestamp."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT INTO readings (timestamp, temp, hum, soil_moisture) VALUES (?, ?, ?, ?)",
                     (datetime.now(), temp, hum, soil_moisture))
        conn.commit()

def cleanup_old_data():
    """Drops readings older than 120 days to save space."""
    cutoff = datetime.now() - timedelta(days=120)
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("DELETE FROM readings WHERE timestamp < ?", (cutoff,))
        conn.commit()
