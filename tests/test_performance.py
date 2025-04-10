import sys
import os
import sqlite3
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import database
import hashlib
import datetime

USER_ID = "TESTUSER"

def setup_user_and_notes():
    os.makedirs("database_file", exist_ok=True)

    conn = sqlite3.connect("database_file/users.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS users;")
    c.execute("CREATE TABLE users (id TEXT PRIMARY KEY, pw TEXT);")
    pw_hash = hashlib.sha256("password".encode()).hexdigest()
    c.execute("INSERT INTO users VALUES (?, ?);", (USER_ID, pw_hash))
    conn.commit()
    conn.close()

    conn = sqlite3.connect("database_file/notes.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS notes;")
    c.execute("CREATE TABLE notes (user TEXT, timestamp TEXT, note TEXT, note_id TEXT);")
    for i in range(10):
        ts = str(datetime.datetime.now())
        note_id = hashlib.sha256(f"{USER_ID}{ts}".encode()).hexdigest()
        c.execute("INSERT INTO notes VALUES (?, ?, ?, ?);", (USER_ID, ts, f"Note {i}", note_id))
    conn.commit()
    conn.close()

    conn = sqlite3.connect("database_file/images.db")
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
    benchmark(lambda: database.verify(USER_ID, "password"))


@pytest.mark.benchmark(group="notes")
def test_write_note_performance(benchmark):
    setup_user_and_notes()
    benchmark(lambda: database.write_note_into_db(USER_ID, "Une note de test"))


@pytest.mark.benchmark(group="notes")
def test_read_notes_performance(benchmark):
    setup_user_and_notes()
    benchmark(lambda: database.read_note_from_db(USER_ID))


@pytest.mark.benchmark(group="images")
def test_list_images_performance(benchmark):
    setup_user_and_notes()
    benchmark(lambda: database.list_images_for_user(USER_ID))
