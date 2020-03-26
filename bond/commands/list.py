from .base_command import BaseCommand
from bond.database import BondDatabase
from bond.cli.table import Table


class ListCommand(BaseCommand):
    subcmd = "list"
    help = "List Bonds in local database."
    arguments = {"--clear": {"action": "store_true", "help": "clear discovered Bonds"}}

    def run(self, args):
        if args.clear:
            BondDatabase().pop("bonds", None)
            print("Cleared discovered Bonds")
        else:
            table = Table(["bondid", "ip", "token"])
            bonds = BondDatabase.get_bonds()
            for bondid in bonds.keys():
                b = bonds[bondid]
                table.add_row(
                    {"bondid": bondid, "ip": b.get("ip"), "token": b.get("token")}
                )


def register():
    ListCommand()
