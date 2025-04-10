import sqlite3
import datetime

from config import get_db_path

def log_event(user_id, action):
    conn = sqlite3.connect(get_db_path("users"))
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS logs (user_id TEXT, action TEXT, timestamp TEXT);")
    c.execute("INSERT INTO logs VALUES (?, ?, ?);", (
        user_id, action, str(datetime.datetime.now())
    ))
    conn.commit()
    conn.close()

def get_logs():
    conn = sqlite3.connect(get_db_path("users"))
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS logs (user_id TEXT, action TEXT, timestamp TEXT);")
    c.execute("SELECT user_id, action, timestamp FROM logs ORDER BY timestamp DESC;")
    logs = c.fetchall()
    conn.close()
    return logs
