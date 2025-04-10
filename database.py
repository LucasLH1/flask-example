# import sqlite3
# import hashlib
# import datetime
#
# user_db_file_location = "database_file/users.db"
# note_db_file_location = "database_file/notes.db"
# image_db_file_location = "database_file/images.db"
#
#
# def list_users():
#     _conn = sqlite3.connect(user_db_file_location)
#     _c = _conn.cursor()
#
#     _c.execute("SELECT id FROM users;")
#     result = [x[0] for x in _c.fetchall()]
#
#     _conn.close()
#
#     return result
#
#
# def verify(id, pw):
#     _conn = sqlite3.connect(user_db_file_location)
#     _c = _conn.cursor()
#
#     _c.execute("SELECT pw FROM users WHERE id = ?;", (id,))
#     result = _c.fetchone()
#
#     _conn.close()
#
#     if result is None:
#         return False
#
#     return result[0] == hashlib.sha256(pw.encode()).hexdigest()
#
#
# def delete_user_from_db(id):
#     _conn = sqlite3.connect(user_db_file_location)
#     _c = _conn.cursor()
#     _c.execute("DELETE FROM users WHERE id = ?;", (id,))
#     _conn.commit()
#     _conn.close()
#
#     # when we delete a user FROM database USERS, we also need to delete all his or her notes data FROM database NOTES
#     _conn = sqlite3.connect(note_db_file_location)
#     _c = _conn.cursor()
#     _c.execute("DELETE FROM notes WHERE user = ?;", (id,))
#     _conn.commit()
#     _conn.close()
#
#     # when we delete a user FROM database USERS, we also need to
#     # [1] delete all his or her images FROM image pool (done in app.py)
#     # [2] delete all his or her images records FROM database IMAGES
#     _conn = sqlite3.connect(image_db_file_location)
#     _c = _conn.cursor()
#     _c.execute("DELETE FROM images WHERE owner = ?;", (id,))
#     _conn.commit()
#     _conn.close()
#
#
# def add_user(id, pw):
#     _conn = sqlite3.connect(user_db_file_location)
#     _c = _conn.cursor()
#
#     _c.execute("INSERT INTO users values(?, ?)", (id.upper(), hashlib.sha256(pw.encode()).hexdigest()))
#
#     _conn.commit()
#     _conn.close()
#
#
# def read_note_from_db(id):
#     _conn = sqlite3.connect(note_db_file_location)
#     _c = _conn.cursor()
#
#     _c.execute("SELECT note_id, timestamp, note FROM notes WHERE user = ?;", (id.upper(),))
#     result = _c.fetchall()
#
#     _conn.commit()
#     _conn.close()
#
#     return result
#
#
# def match_user_id_with_note_id(note_id):
#     # Given the note id, confirm if the current user is the owner of the note which is being operated.
#     _conn = sqlite3.connect(note_db_file_location)
#     _c = _conn.cursor()
#
#     _c.execute("SELECT user FROM notes WHERE note_id = ?;", (note_id,))
#     result = _c.fetchone()[0]
#
#     _conn.commit()
#     _conn.close()
#
#     return result
#
#
# def write_note_into_db(id, note_to_write):
#     _conn = sqlite3.connect(note_db_file_location)
#     _c = _conn.cursor()
#
#     current_timestamp = str(datetime.datetime.now())
#     _c.execute("INSERT INTO notes values(?, ?, ?, ?)", (
#     id.upper(), current_timestamp, note_to_write, hashlib.sha256((id.upper() + current_timestamp).encode()).hexdigest()))
#
#     _conn.commit()
#     _conn.close()
#
#
# def delete_note_from_db(note_id):
#     _conn = sqlite3.connect(note_db_file_location)
#     _c = _conn.cursor()
#
#     _c.execute("DELETE FROM notes WHERE note_id = ?;", (note_id,))
#
#     _conn.commit()
#     _conn.close()
#
#
# def image_upload_record(uid, owner, image_name, timestamp):
#     _conn = sqlite3.connect(image_db_file_location)
#     _c = _conn.cursor()
#
#     _c.execute("INSERT INTO images VALUES (?, ?, ?, ?)", (uid, owner, image_name, timestamp))
#
#     _conn.commit()
#     _conn.close()
#
#
# def list_images_for_user(owner):
#     _conn = sqlite3.connect(image_db_file_location)
#     _c = _conn.cursor()
#
#     _c.execute("SELECT uid, timestamp, name FROM images WHERE owner = ?;", (owner,))
#     result = _c.fetchall()
#
#     _conn.commit()
#     _conn.close()
#
#     return result
#
#
# def match_user_id_with_image_uid(image_uid):
#     # Given the note id, confirm if the current user is the owner of the note which is being operated.
#     _conn = sqlite3.connect(image_db_file_location)
#     _c = _conn.cursor()
#
#     _c.execute("SELECT uid, timestamp, name FROM images WHERE owner = ?;", (owner,))
#     result = _c.fetchone()[0]
#
#     _conn.commit()
#     _conn.close()
#
#     return result
#
#
# def delete_image_from_db(image_uid):
#     _conn = sqlite3.connect(image_db_file_location)
#     _c = _conn.cursor()
#
#     _c.execute("DELETE FROM images WHERE uid = ?;", (image_uid,))
#
#     _conn.commit()
#     _conn.close()
#
# def log_event(user_id, action):
#     import datetime
#     conn = sqlite3.connect(user_db_file_location)
#     c = conn.cursor()
#     c.execute("CREATE TABLE IF NOT EXISTS logs (user_id TEXT, action TEXT, timestamp TEXT);")
#     c.execute("INSERT INTO logs VALUES (?, ?, ?);", (
#         user_id, action, str(datetime.datetime.now())
#     ))
#     conn.commit()
#     conn.close()
#
# def get_logs():
#     conn = sqlite3.connect(user_db_file_location)
#     c = conn.cursor()
#     c.execute("CREATE TABLE IF NOT EXISTS logs (user_id TEXT, action TEXT, timestamp TEXT);")
#     c.execute("SELECT user_id, action, timestamp FROM logs ORDER BY timestamp DESC;")
#     results = c.fetchall()
#     conn.close()
#     return results
#
#
# if __name__ == "__main__":
#     print(list_users())
