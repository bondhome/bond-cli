from .database import get, set

def get_assert_selected_bondid():
    selected_bondid = get('selected_bondid')
    if not selected_bondid:
        raise Exception("No Bond selected. Use 'bond select' first.")
    return selected_bondid

def get_bonds():
    bonds = get('bonds')
    if not bonds:
        bonds = {}
        set('bonds', bonds)
    return bonds
