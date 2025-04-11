import sqlite3
from config import get_db_path
from repositories.security import hash_password
import logging
logger = logging.getLogger("flask_app")

def list_users():
    conn = sqlite3.connect(get_db_path("users"))
    c = conn.cursor()
    c.execute("SELECT id FROM users;")
    result = [x[0] for x in c.fetchall()]
    conn.close()
    return result

def verify(id, pw):
    conn = sqlite3.connect(get_db_path("users"))
    c = conn.cursor()
    c.execute("SELECT pw FROM users WHERE id = ?;", (id,))
    result = c.fetchone()
    conn.close()
    if result is None:
        return False
    return result[0] == hash_password(pw)

def add_user(id, pw):
    conn = sqlite3.connect(get_db_path("users"))
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?)", (id.upper(), hash_password(pw)))
    conn.commit()
    conn.close()

def delete_user(id):
    conn = sqlite3.connect(get_db_path("users"))
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?;", (id,))
    conn.commit()
    conn.close()
