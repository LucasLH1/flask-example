import unittest
import os
import sqlite3
from config import get_db_path
from repositories.user_repository import add_user, verify, list_users

class TestUserManagement(unittest.TestCase):
    def setUp(self):
        self.db_path = get_db_path("users")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS users;")
        c.execute("CREATE TABLE users (id TEXT PRIMARY KEY, pw TEXT);")
        conn.commit()
        conn.close()

    def tearDown(self):
        if "test" in self.db_path and os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_add_user_should_create_user_entry(self):
        add_user("alice", "secret")
        users = list_users()
        self.assertIn("ALICE", users)

    def test_verify_should_return_true_for_correct_password(self):
        add_user("bob", "password123")
        self.assertTrue(verify("BOB", "password123"))

    def test_verify_should_return_false_for_wrong_password(self):
        add_user("charlie", "mysecurepwd")
        self.assertFalse(verify("CHARLIE", "wrongpwd"))

if __name__ == "__main__":
    unittest.main()
