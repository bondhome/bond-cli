import bond.database
from bond.proto.http import HTTP_Transport

def get_bonds():
    selected_bondid = bond.database.get('selected_bondid')
    if not selected_bondid:
        return bond.database.get('mdns_cache').keys()
    else:
        return [selected_bondid]

def get_all_async(**kwargs):
    return [
        HTTP_Transport(
            bondid=bondid,
            port = 80,
            token = '',
            ).get_async(**kwargs)
        for bondid in get_bonds()
    ]
