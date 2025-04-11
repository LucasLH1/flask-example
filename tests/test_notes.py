import unittest
import os
import sqlite3
from config import get_db_path
from repositories.note_repository import write_note, read_notes, delete_note

class TestNoteManagement(unittest.TestCase):
    def setUp(self):
        self.db_path = get_db_path("notes")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS notes;")
        c.execute("CREATE TABLE notes (user TEXT, timestamp TEXT, note TEXT, note_id TEXT);")
        conn.commit()
        conn.close()

    def tearDown(self):
        if "test" in self.db_path and os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_write_and_read_note(self):
        write_note("alice", "Ma première note")
        notes = read_notes("ALICE")
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0][2], "Ma première note")

    def test_delete_note(self):
        write_note("DELUSER", "Note à supprimer")
        notes = read_notes("DELUSER")
        note_id = notes[0][0]
        delete_note(note_id)
        self.assertEqual(len(read_notes("DELUSER")), 0)

if __name__ == "__main__":
    unittest.main()
