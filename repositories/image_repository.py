import sqlite3
import datetime

from config import get_db_path

def upload_image(uid, owner, name, timestamp=None):
    timestamp = timestamp or str(datetime.datetime.now())
    conn = sqlite3.connect(get_db_path("images"))
    c = conn.cursor()
    c.execute("INSERT INTO images VALUES (?, ?, ?, ?)", (uid, owner, name, timestamp))
    conn.commit()
    conn.close()

def list_images(owner):
    conn = sqlite3.connect(get_db_path("images"))
    c = conn.cursor()
    c.execute("SELECT uid, timestamp, name FROM images WHERE owner = ?;", (owner,))
    images = c.fetchall()
    conn.close()
    return images

def delete_image(image_uid):
    conn = sqlite3.connect(get_db_path("images"))
    c = conn.cursor()
    c.execute("DELETE FROM images WHERE uid = ?;", (image_uid,))
    conn.commit()
    conn.close()

def match_user_with_image_uid(image_uid):
    conn = sqlite3.connect(get_db_path("images"))
    c = conn.cursor()
    c.execute("SELECT owner FROM images WHERE uid = ?;", (image_uid,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
