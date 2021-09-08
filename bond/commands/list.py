from bond.cli.table import Table
from bond.database import BondDatabase

from .base_command import BaseCommand


class ListCommand(BaseCommand):
    subcmd = "list"
    help = "List Bonds in local database."
    arguments = {
        "--forget-all": {"action": "store_true",
                         "help": "forget all Bonds and associated shadows"},
        "--forget": {"help": "forget specified Bond ID"}
    }

    def run(self, args):
        if args.forget_all:
            BondDatabase().pop("bonds", None)
            print("Cleared discovered Bonds")
        elif args.forget:
            BondDatabase().set_bond(args.forget, "token", None)
            print("Forgot %s." % args.forget)
        else:
            table = Table(["bondid", "ip", "token"])
            bonds = BondDatabase.get_bonds(require_token=True)
            for bondid in bonds.keys():
                b = bonds[bondid]
                table.add_row(
                    {"bondid": bondid, "ip": b.get("ip"), "token": b.get("token")}
                )


def register():
    ListCommand()
