import json
import os
from threading import RLock
from collections.abc import MutableMapping

DB_FILENAME = os.path.expanduser("~/.bond/db.json")
DB_DIRNAME = os.path.dirname(DB_FILENAME)


class BondDatabase(MutableMapping):

    __instance = None

    def __init__(self):
        if BondDatabase.__instance is not None:
            raise Exception("This class is a singleton!")
        self.lock = RLock()
        # TODO: handle the corner case where the path exists, but it is not a file
        if os.path.exists(DB_FILENAME):
            with open(DB_FILENAME) as db_file:
                self.db = json.load(db_file)
        else:
            os.makedirs(DB_DIRNAME, exist_ok=True)
            self.db = dict()
            self.__save()
        BondDatabase.__instance = self

    def __save(self):
        with self.lock:
            with open(DB_FILENAME, "w") as f:
                json.dump(db, f, indent=2)

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
    
    def __iter__(self):
        return self.db.__iter__()

    def __len__(self):
        return len(self.db)
    
    
    # Singleton static methods


    @staticmethod
    def get_assert_selected_bondid(self):
        selected_bondid = BondDatabase.get("selected_bondid")
        if not selected_bondid:
            raise Exception("No Bond selected. Use 'bond select' first.")
        return selected_bondid

    @staticmethod
    def get_bonds(self):
        return BondDatabase.load().setdefault("bonds", dict())

    @staticmethod
    def get_bond(bondid):
        return BondDatabase.get_bonds().get(bondid, dict())

    @staticmethod
    def set_bond(bondid, key, value):
        bonds = BondDatabase.get_bonds()
        bonds.setdefault(bondid, dict())
        bonds[bondid][key] = value
        BondDatabase.set("bonds", bonds)

    @staticmethod
    def load():
        if BondDatabase.__instance is None:
            BondDatabase()
        return BondDatabase.__instance

    @staticmethod
    def get(key):
        return BondDatabase.load().get(key)

    @staticmethod
    def set(key):
        return BondDatabase.load().set(key)
