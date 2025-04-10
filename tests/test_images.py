import unittest
import os
import sqlite3
from config import get_db_path
from repositories.image_repository import upload_image, list_images, delete_image

class TestImageManagement(unittest.TestCase):
    def setUp(self):
        self.db_path = get_db_path("images")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS images;")
        c.execute("CREATE TABLE images (uid TEXT, owner TEXT, name TEXT, timestamp TEXT);")
        conn.commit()
        conn.close()

    def tearDown(self):
        if "test" in self.db_path and os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_upload_and_list_image(self):
        upload_image("img123", "ALICE", "chat.jpg", "2024-04-09 15:00:00")
        images = list_images("ALICE")
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0][0], "img123")

    def test_delete_image(self):
        uid = "img456"
        upload_image(uid, "BOB", "chien.png", "2024-04-09 16:00:00")
        self.assertEqual(len(list_images("BOB")), 1)
        delete_image(uid)
        self.assertEqual(len(list_images("BOB")), 0)

if __name__ == "__main__":
    unittest.main()
