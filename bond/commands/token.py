from .base_command import BaseCommand
from bond.database import BondDatabase
from bond.cli.console import LogLine


def update_token(token):
    bondid = BondDatabase.get_assert_selected_bondid()
    bonds = BondDatabase.get_bonds()
    if bondid not in bonds.keys():
        bonds[bondid] = dict()
    bonds[bondid]["token"] = token
    print(f"Updated token for {bondid}")
    BondDatabase.set("bonds", bonds)


class TokenCommand(BaseCommand):
    subcmd = "token"
    help = "Manage token-based authentication."
    arguments = {"TOKEN": {"help": "Save Bond token to local database"}}

    def run(self, args):
        update_token(args["Token"])


def register():
    TokenCommand()
