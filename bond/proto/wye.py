from bond.database import BondDatabase
from bond.proto.http import HTTP_Transport


def get_bonds():
    selected_bondid = BondDatabase().get("selected_bondid")
    if not selected_bondid:
        return BondDatabase.get_bonds().keys()
    else:
        return [selected_bondid]


def mk_transport(bondid):
    b = BondDatabase.get_bonds()[bondid]
    return HTTP_Transport(
        bondid=bondid,
        hostname=b["ip"],
        port=b["port"],
        token=b["token"] if "token" in b else None,
    )


def get(bondid, **kwargs):
    return mk_transport(bondid).get(**kwargs)


def put(bondid, **kwargs):
    return mk_transport(bondid).put(**kwargs)


def post(bondid, **kwargs):
    return mk_transport(bondid).post(**kwargs)


def patch(bondid, **kwargs):
    return mk_transport(bondid).patch(**kwargs)


def delete(bondid, **kwargs):
    return mk_transport(bondid).delete(**kwargs)


def request_async(http_method_name, bondid, **kwargs):
    caller_on_success = kwargs["on_success"]

    def success_wrapper(bondid, rsp):
        if rsp["s"] > 299:
            msg = "%s: Error %d" % (bondid, rsp["s"])
            kwargs["on_error"](bondid, Exception(msg))
        else:
            caller_on_success(bondid, rsp)

    kwargs["on_success"] = success_wrapper
    try:
        return mk_transport(bondid).request_async(http_method_name, **kwargs)
    except KeyError:
        kwargs["on_error"](
            bondid,
            Exception(
                f"{bondid} hasn't been discovered by bond-cli ('bond discover')."
            ),
        )


def get_all_async(**kwargs):
    return [
        request_async("get", bondid, **kwargs) for bondid in BondDatabase.get_bonds()
    ]
