import sqlite3
import datetime

from config import get_db_path
from repositories.security import generate_sha256_id


def write_note(user_id, note_text):
    conn = sqlite3.connect(get_db_path("notes"))
    c = conn.cursor()
    timestamp = str(datetime.datetime.now())
    note_id = generate_sha256_id(user_id.upper() + timestamp)
    c.execute("INSERT INTO notes VALUES (?, ?, ?, ?)", (user_id.upper(), timestamp, note_text, note_id))
    conn.commit()
    conn.close()

def read_notes(user_id):
    conn = sqlite3.connect(get_db_path("notes"))
    c = conn.cursor()
    c.execute("SELECT note_id, timestamp, note FROM notes WHERE user = ?;", (user_id.upper(),))
    notes = c.fetchall()
    conn.close()
    return notes

def delete_note(note_id):
    conn = sqlite3.connect(get_db_path("notes"))
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE note_id = ?;", (note_id,))
    conn.commit()
    conn.close()

def match_user_with_note(note_id):
    conn = sqlite3.connect(get_db_path("notes"))
    c = conn.cursor()
    c.execute("SELECT user FROM notes WHERE note_id = ?;", (note_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
