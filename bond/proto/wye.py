import bond.database
from bond.proto.http import HTTP_Transport

def get_bonds():
    selected_bondid = bond.database.get('selected_bondid')
    if not selected_bondid:
        return bond.database.get_bonds().keys()
    else:
        return [selected_bondid]

def get_async(bondid, **kwargs):
    caller_on_success = kwargs['on_success']
    def success_wrapper(bondid, rsp):
        if rsp['s'] > 299:
            msg = '%s: Error %d' % (bondid, rsp['s'])
            kwargs['on_error'](bondid, Exception(msg))
        else:
            caller_on_success(bondid, rsp)
    kwargs['on_success'] = success_wrapper
    b = bond.database.get_bond(bondid)
    return HTTP_Transport(
            bondid = bondid,
            hostname = b['ip'],
            port = b['port'],
            token = b['token'] if 'token' in b else None,
            ).get_async(**kwargs)

def get_all_async(**kwargs):
    return [ get_async(bondid, **kwargs) for bondid in get_bonds() ]
