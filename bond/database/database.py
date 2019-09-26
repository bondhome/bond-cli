import json
import os
import threading

db = dict()

DB_FILENAME = os.path.expanduser("~/.bond/db.json")
DB_DIRNAME = os.path.dirname(DB_FILENAME)

lock = threading.RLock()


def load():
    global db
    try:
        with open(DB_FILENAME) as f:
            db = json.load(f)
    except FileNotFoundError:
        if not os.path.exists(DB_DIRNAME):
            os.makedirs(DB_DIRNAME)
        _save()


def _save():
    with open(DB_FILENAME, "w") as f:
        json.dump(db, f, indent=2)


def set(key, value):
    db[key] = value
    _save()


def get(key):
    if key in db:
        return db[key]
    else:
        return None
