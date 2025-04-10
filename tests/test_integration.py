import unittest
from unittest.mock import patch, MagicMock
import hashlib
from repositories.user_repository import add_user, verify
from repositories.note_repository import delete_note
from repositories.image_repository import upload_image

class IntegrationDatabaseMockTests(unittest.TestCase):

    @patch("sqlite3.connect")
    def test_verify_success(self, mock_connect):
        mock_cursor = MagicMock()
        hashed_pw = hashlib.sha256("password".encode()).hexdigest()
        mock_cursor.fetchone.return_value = (hashed_pw,)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        result = verify("USER1", "password")
        self.assertTrue(result)

        mock_cursor.execute.assert_called_once_with(
            "SELECT pw FROM users WHERE id = ?;", ("USER1",)
        )
        mock_conn.close.assert_called_once()

    @patch("sqlite3.connect")
    def test_verify_user_not_found(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        result = verify("USER1", "password")
        self.assertFalse(result)

    @patch("sqlite3.connect")
    def test_add_user_executes_insert(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        add_user("USER1", "password")

        expected_hash = hashlib.sha256("password".encode()).hexdigest()
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO users VALUES (?, ?)", ("USER1", expected_hash)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("sqlite3.connect")
    def test_delete_note_from_db_executes_correctly(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        delete_note("note-id-123")

        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM notes WHERE note_id = ?;", ("note-id-123",)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("sqlite3.connect")
    def test_image_upload_record_executes_correctly(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        upload_image("img001", "ALICE", "photo.jpg", "2024-04-09 12:00")

        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO images VALUES (?, ?, ?, ?)",
            ("img001", "ALICE", "photo.jpg", "2024-04-09 12:00")
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()
