import bond.database
from bond.proto.http import HTTP_Transport

def get_bonds():
    selected_bondid = bond.database.get('selected_bondid')
    if not selected_bondid:
        return bond.database.get_bonds().keys()
    else:
        return [selected_bondid]

def get_all_async(**kwargs):
    return [
        HTTP_Transport(
            bondid = bondid,
            hostname = bond.database.get_bond(bondid)['ip'],
            port = bond.database.get_bond(bondid)['port'],
            token = '',
            ).get_async(**kwargs)
        for bondid in get_bonds()
    ]
