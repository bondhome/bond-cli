from .base_command import BaseCommand
from bond.database import BondDatabase
from bond.cli.console import LogLine
import bond.proto


def update_token(token, bond_id=None):
    bond_id = bond_id or BondDatabase.get_assert_selected_bondid()
    bonds = BondDatabase.get_bonds()
    if bond_id not in bonds.keys():
        bonds[bond_id] = dict()
    bonds[bond_id]["token"] = token
    print("Updated token for %s" % bondid)
    BondDatabase.set("bonds", bonds)


def check_unlocked_token(bond_id=None):
    bond_id = bond_id or BondDatabase.get_assert_selected_bondid()
    rsp = bond.proto.get(bond_id, topic="token")
    token = rsp.get("b", {}).get("token")
    if token:
        print("%s's token is unlocked, updating..." % bond_id)
        update_token(token, bond_id)
    else:
        print("%s's token is not unlocked." % bond_id)
        print("Set it manually with 'bond token <token>',")
        print("or unlock the token and run 'bond token'")
        print("(tip: the token is unlocked for a short period after a reboot)")


class TokenCommand(BaseCommand):
    subcmd = "token"
    help = "Manage token-based authentication."
    arguments = {"token": {"help": "Save Bond token to local database", "nargs": "?"}}

    def run(self, args):
        if args.token:
            update_token(args.token)
        else:
            check_unlocked_token()

def register():
    TokenCommand()
