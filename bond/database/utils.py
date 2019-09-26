from .database import get, set, lock


def get_assert_selected_bondid():
    selected_bondid = get("selected_bondid")
    if not selected_bondid:
        raise Exception("No Bond selected. Use 'bond select' first.")
    return selected_bondid


def get_bonds():
    with lock:
        bonds = get("bonds")
        if not bonds:
            bonds = dict()
            set("bonds", bonds)
        return bonds


def get_bond(bondid):
    bonds = get_bonds()
    if bondid not in bonds:
        return dict()
    else:
        return bonds[bondid]


def set_bond(bondid, key, value):
    with lock:
        bonds = get_bonds()
        if bondid not in bonds:
            bonds[bondid] = dict()
        bonds[bondid][key] = value
        set("bonds", bonds)
