import bond.proto
from bond.database import BondDatabase


def update_token(token, bond_id=None):
    bond_id = bond_id or BondDatabase.get_assert_selected_bondid()
    bonds = BondDatabase.get_bonds()
    if bond_id not in bonds.keys():
        bonds[bond_id] = dict()
    bonds[bond_id]["token"] = token
    print(f"Updated token for {bond_id}: {token}")
    BondDatabase.set("bonds", bonds)


def check_unlocked_token(bond_id=None):
    bond_id = bond_id or BondDatabase.get_assert_selected_bondid()
    rsp = bond.proto.get(bond_id, topic="token")
    token = rsp.get("b", {}).get("token")
    if token:
        update_token(token, bond_id)
    return token is not None


def unlock_token(bond_id=None, pin=None):
    bond_id = bond_id or BondDatabase.get_assert_selected_bondid()
    if not pin:
        pin = input("Enter Bond PIN: ")
    rsp = bond.proto.patch(bond_id, topic="token", body={"pin": pin, "locked": 0})
    token = rsp.get("b", {}).get("token")
    if token:
        update_token(token, bond_id)
    return token is not None


def check_stored_token(bond_id=None):
    """Probe the locally-stored token against the Bond.

    Returns True if the Bond accepts the saved token, False if it rejects it
    (obsolete), or None if the Bond couldn't be reached to tell. Any endpoint
    other than /sys/version and /token requires the token, so 'devices' is a
    reliable probe: a valid token returns 2xx, an obsolete one returns 401.
    """
    bond_id = bond_id or BondDatabase.get_assert_selected_bondid()
    try:
        rsp = bond.proto.get(bond_id, topic="devices")
    except PermissionError:
        return False
    except Exception:
        return None
    status = rsp.get("s")
    if status == 401:
        return False
    if status is not None and 200 <= status <= 299:
        return True
    return None


class TokenCommand(object):
    subcmd = "token"
    help = "Manage token-based authentication."
    arguments = {
        "token": {"help": "Save Bond token to local database", "nargs": "?"},
        "--pin": {
            "nargs": "?",
            "const": "",
            "help": "unlock token with the Bond PIN (prompts for the PIN if no value is given)",
        },
        "--bond-id": {"help": "ignore selected Bond and use provided"},
    }

    def run(self, args):
        bond_id = args.bond_id or BondDatabase.get_assert_selected_bondid()
        if args.token:
            update_token(args.token, bond_id)
        elif args.pin is not None:
            print("Unlocking token...")
            if not unlock_token(bond_id, args.pin):
                print(f"Failed to unlock {bond_id}'s token. Check the PIN and try again.")
        elif not check_unlocked_token(bond_id):
            stored_token = BondDatabase.get_bond(bond_id).get("token")
            if not stored_token:
                print(f"{bond_id}'s token is not unlocked, and none is saved locally.")
                print("Unlock it with the Bond PIN: 'bond token --pin'")
                print("(tip: the token is also unlocked for a short period after a reboot)")
            else:
                valid = check_stored_token(bond_id)
                if valid is True:
                    print(f"{bond_id}'s saved token is still valid: {stored_token}")
                elif valid is False:
                    print(f"{bond_id}'s saved token is obsolete: {stored_token}")
                    print("Get a new one with 'bond token --pin', set it manually with 'bond token <token>',")
                    print("or power-cycle the Bond and run 'bond token' (unlocked briefly after a reboot).")
                else:
                    print(f"Couldn't reach {bond_id} to check whether its saved token is still valid: {stored_token}")
