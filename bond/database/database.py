import json
import os
from collections.abc import MutableMapping
from threading import RLock

DB_FILENAME = os.path.expanduser("~/.bond/db.json")
DB_DIRNAME = os.path.dirname(DB_FILENAME)


class BondDatabase(MutableMapping):

    __instance = None

    def __new__(cls):
        """Takes the place of __init__ to only return a single instance of the database.
        That is, BondDatabase() is a singleton.
        Note: any initialization should go here, not in a new __init__ function.
              any __init__ for this class will be called *on every return value of
              this function*!"""
        if cls.__instance is None:
            cls.__instance = super(BondDatabase, cls).__new__(cls)
            cls.__instance.lock = RLock()
            if os.path.exists(DB_FILENAME):
                with open(DB_FILENAME) as db_file:
                    cls.__instance.db = json.load(db_file)
            else:
                os.makedirs(DB_DIRNAME, exist_ok=True)
                cls.__instance.db = dict()
                cls.__instance.__save()
        return cls.__instance

    def __save(self):
        with self.lock:
            with open(DB_FILENAME, "w") as f:
                json.dump(self.db, f, indent=2)

    def __setitem__(self, key, value):
        with self.lock:
            self.db[key] = value
            self.__save()

    def __getitem__(self, key):
        with self.lock:
            return self.db[key]

    def __delitem__(self, key):
        with self.lock:
            del self.db[key]
            self.__save()

    def __iter__(self):
        return self.db.__iter__()

    def __len__(self):
        return len(self.db)

    # Singleton static methods

    @staticmethod
    def get_assert_selected_bondid():
        selected_bondid = BondDatabase().get("selected_bondid")
        if selected_bondid is None:
            raise SystemExit("No Bond selected. Use 'bond select' first.")
        return selected_bondid

    @staticmethod
    def get_bonds():
        return BondDatabase().setdefault("bonds", dict())

    @staticmethod
    def get_bond(bondid):
        return BondDatabase().get_bonds().get(bondid, dict())

    @staticmethod
    def set_bond(bondid, key, value):
        bonds = BondDatabase.get_bonds()
        bonds.setdefault(bondid, dict())
        bonds[bondid][key] = value
        BondDatabase.set("bonds", bonds)

    @staticmethod
    def set(key, value):
        BondDatabase()[key] = value
