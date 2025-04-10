import os

SECRET_KEY = "fdsafasd"
UPLOAD_FOLDER = "image_pool"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

ENV = os.getenv("FLASK_ENV", "development")

DATABASE_PATHS = {
    "users": {
        "development": "database_file/users.db",
        "test": "tests/database_file/users.db"
    },
    "notes": {
        "development": "database_file/notes.db",
        "test": "tests/database_file/notes.db"
    },
    "images": {
        "development": "database_file/images.db",
        "test": "tests/database_file/images.db"
    }
}

def get_db_path(name):
    return DATABASE_PATHS[name][ENV]
