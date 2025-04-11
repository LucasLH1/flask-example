import cProfile
import pstats
import database
import random
import string
import sqlite3

NB_USERS = 10
NOTES_PER_USER = 10

def random_note():
    return "Note : " + ''.join(random.choices(string.ascii_letters + string.digits, k=20))

def simulate_usage():
    users = []

    for i in range(NB_USERS):
        uid = f"USER{i}"
        pw = "pass123"
        try:
            database.add_user(uid, pw)
        except sqlite3.IntegrityError:
            pass
        users.append(uid)

    for uid in users:
        for _ in range(NOTES_PER_USER):
            database.write_note_into_db(uid, random_note())

    for uid in users:
        _ = database.read_note_from_db(uid)

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    simulate_usage()

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumulative')
    stats.dump_stats('simulate_usage_after.prof')
