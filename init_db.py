import sqlite3
import os

os.makedirs("database_file", exist_ok=True)

def init_users_db():
    conn = sqlite3.connect("database_file/users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            pw TEXT
        );
    """)
    conn.commit()
    conn.close()

def init_notes_db():
    conn = sqlite3.connect("database_file/notes.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            user TEXT,
            timestamp TEXT,
            note TEXT,
            note_id TEXT
        );
    """)
    conn.commit()
    conn.close()

def init_images_db():
    conn = sqlite3.connect("database_file/images.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS images (
            uid TEXT,
            owner TEXT,
            name TEXT,
            timestamp TEXT
        );
    """)
    conn.commit()
    conn.close()

def init_all():
    init_users_db()
    init_notes_db()
    init_images_db()

if __name__ == "__main__":
    init_all()
