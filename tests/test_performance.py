import sys
import os
import sqlite3
import pytest
import hashlib
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import get_db_path
from repositories.user_repository import verify
from repositories.note_repository import write_note, read_notes
from repositories.image_repository import list_images

USER_ID = "TESTUSER"

def setup_user_and_notes():
    user_db = get_db_path("users")
    os.makedirs(os.path.dirname(user_db), exist_ok=True)
    conn = sqlite3.connect(user_db)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS users;")
    c.execute("CREATE TABLE users (id TEXT PRIMARY KEY, pw TEXT);")
    pw_hash = hashlib.sha256("password".encode()).hexdigest()
    c.execute("INSERT INTO users VALUES (?, ?);", (USER_ID, pw_hash))
    conn.commit()
    conn.close()

    note_db = get_db_path("notes")
    conn = sqlite3.connect(note_db)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS notes;")
    c.execute("CREATE TABLE notes (user TEXT, timestamp TEXT, note TEXT, note_id TEXT);")
    for i in range(10):
        ts = str(datetime.datetime.now())
        note_id = hashlib.sha256(f"{USER_ID}{ts}".encode()).hexdigest()
        c.execute("INSERT INTO notes VALUES (?, ?, ?, ?);", (USER_ID, ts, f"Note {i}", note_id))
    conn.commit()
    conn.close()

    image_db = get_db_path("images")
    conn = sqlite3.connect(image_db)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS images;")
    c.execute("CREATE TABLE images (uid TEXT, owner TEXT, name TEXT, timestamp TEXT);")
    for i in range(5):
        c.execute("INSERT INTO images VALUES (?, ?, ?, ?);", (
            f"img{i}", USER_ID, f"img_{i}.jpg", str(datetime.datetime.now())))
    conn.commit()
    conn.close()

@pytest.mark.benchmark(group="auth")
def test_verify_performance(benchmark):
    setup_user_and_notes()
    benchmark(lambda: verify(USER_ID, "password"))

@pytest.mark.benchmark(group="notes")
def test_write_note_performance(benchmark):
    setup_user_and_notes()
    benchmark(lambda: write_note(USER_ID, "Une note de test"))

@pytest.mark.benchmark(group="notes")
def test_read_notes_performance(benchmark):
    setup_user_and_notes()
    benchmark(lambda: read_notes(USER_ID))

@pytest.mark.benchmark(group="images")
def test_list_images_performance(benchmark):
    setup_user_and_notes()
    benchmark(lambda: list_images(USER_ID))
