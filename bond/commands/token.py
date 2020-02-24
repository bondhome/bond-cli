from .base_command import BaseCommand
import bond.database
from bond.cli.console import LogLine


def update_token(token):
    bondid = bond.database.get_assert_selected_bondid()
    bonds = bond.database.get_bonds()
    if bondid not in bonds.keys():
        bonds[bondid] = dict()
    bonds[bondid]["token"] = token
    print(f"Updated token for {bondid}")
    bond.database.set("bonds", bonds)


class TokenCommand(BaseCommand):
    subcmd = "token"
    help = "Manage token-based authentication."
    arguments = [(["TOKEN"], {"help": "Save Bond token to local database"})]

    def run(self, args):
        update_token(args["Token"])


def register():
    TokenCommand()
