import unittest
from unittest.mock import patch
import sqlite3
import os
from config import get_db_path
from app import app

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.secret_key = "test_secret"
        self.client = app.test_client()

        users_db = get_db_path("users")
        os.makedirs(os.path.dirname(users_db), exist_ok=True)
        conn = sqlite3.connect(users_db)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, pw TEXT);")
        c.execute("DELETE FROM users;")
        c.execute("INSERT INTO users VALUES (?, ?);", ("ADMIN", "hash"))
        c.execute("INSERT INTO users VALUES (?, ?);", ("TESTUSER", "hash"))
        conn.commit()
        conn.close()

        images_db = get_db_path("images")
        os.makedirs(os.path.dirname(images_db), exist_ok=True)
        conn = sqlite3.connect(images_db)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS images (uid TEXT, owner TEXT, name TEXT, timestamp TEXT);")
        c.execute("DELETE FROM images;")
        conn.commit()
        conn.close()

        notes_db = get_db_path("notes")
        os.makedirs(os.path.dirname(notes_db), exist_ok=True)
        conn = sqlite3.connect(notes_db)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS notes (user TEXT, timestamp TEXT, note TEXT, note_id TEXT);")
        c.execute("DELETE FROM notes;")
        conn.commit()
        conn.close()

    def login_as(self, user_id):
        self.client.post("/login", data={
            "id": user_id.lower(),
            "pw": "password"
        }, follow_redirects=True)

    @patch("app.verify")
    @patch("app.list_users")
    def test_admin_page_shows_user_list(self, mock_list_users, mock_verify):
        mock_list_users.return_value = ["ADMIN", "U1", "U2"]
        mock_verify.return_value = True

        self.login_as("ADMIN")
        response = self.client.get("/admin/", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"U1", response.data)
        self.assertIn(b"U2", response.data)

    @patch("app.add_user")
    @patch("app.verify")
    @patch("app.list_users")
    def test_add_user_post_triggers_add(self, mock_list_users, mock_verify, mock_add_user):
        mock_list_users.return_value = ["ADMIN", "TESTUSER"]
        mock_verify.return_value = True

        self.login_as("ADMIN")
        response = self.client.post("/add_user", data={
            "id": "uniqueuser",
            "pw": "newpassword"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        mock_add_user.assert_called_once_with("UNIQUEUSER", "newpassword")

    @patch("app.verify")
    @patch("app.list_users")
    def test_login_success_sets_session(self, mock_list_users, mock_verify):
        mock_list_users.return_value = ["TESTUSER"]
        mock_verify.return_value = True

        response = self.client.post("/login", data={
            "id": "testuser",
            "pw": "password"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get("_user_id"), "TESTUSER")

    @patch("app.verify")
    @patch("app.list_users")
    def test_login_failure_does_not_set_session(self, mock_list_users, mock_verify):
        mock_list_users.return_value = ["TESTUSER"]
        mock_verify.return_value = False

        response = self.client.post("/login", data={
            "id": "testuser",
            "pw": "wrongpass"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as sess:
            self.assertIsNone(sess.get("_user_id"))

    @patch("app.read_notes")
    @patch("app.list_images")
    @patch("app.verify")
    @patch("app.list_users")
    def test_private_page_shows_notes_and_images(self, mock_list_users, mock_verify, mock_list_images, mock_read_notes):
        mock_list_users.return_value = ["TESTUSER"]
        mock_verify.return_value = True

        self.login_as("TESTUSER")

        mock_read_notes.return_value = [("n1", "2025-04-01", "Test note")]
        mock_list_images.return_value = [("img1", "2025-04-01", "photo.jpg")]

        response = self.client.get("/private/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test note", response.data)
        self.assertIn(b"photo.jpg", response.data)

if __name__ == "__main__":
    unittest.main()
