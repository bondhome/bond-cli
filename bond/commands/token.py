from .base_command import BaseCommand
from bond.database import BondDatabase
import bond.proto


def update_token(token, bond_id=None):
    bond_id = bond_id or BondDatabase.get_assert_selected_bondid()
    bonds = BondDatabase.get_bonds()
    if bond_id not in bonds.keys():
        bonds[bond_id] = dict()
    bonds[bond_id]["token"] = token
    print("Updated token for %s" % bond_id)
    BondDatabase.set("bonds", bonds)


def check_unlocked_token(bond_id=None):
    bond_id = bond_id or BondDatabase.get_assert_selected_bondid()
    rsp = bond.proto.get(bond_id, topic="token")
    token = rsp.get("b", {}).get("token")
    if token:
        update_token(token, bond_id)
    return token is not None


class TokenCommand(BaseCommand):
    subcmd = "token"
    help = "Manage token-based authentication."
    arguments = {"token": {"help": "Save Bond token to local database", "nargs": "?"}}

    def run(self, args):
        bond_id = BondDatabase.get_assert_selected_bondid()
        if args.token:
            update_token(args.token, bond_id)
        elif not check_unlocked_token(bond_id):
            print("%s's token is not unlocked." % bond_id)
            stored_token = BondDatabase.get_bond(bond_id).get("token")
            if stored_token:
                print(
                    "There's already a token for %s in your local database: %s."
                    % (bond_id, stored_token)
                )
                print("If this token is obsolete, you will need to set the new token.")
                print(
                    "You can set it manually with 'bond token <token>', or unlock the token and run 'bond token'"
                )
                print("(tip: the token is unlocked for a short period after a reboot)")


def register():
    TokenCommand()
