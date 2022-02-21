from bond.cli.table import Table
from bond.database import BondDatabase


class BondListCommand(object):
    subcmd = "list"
    help = "List Bonds in local database."
    arguments = {
        "--clear": {"action": "store_true", "help": "clear discovered Bonds"},
        "-q": {"help": "dont print table outline (quiet mode)", "action": "store_true"},
    }

    def run(self, args):
        if args.clear:
            BondDatabase().pop("bonds", None)
            print("Cleared discovered Bonds")
        else:
            table = Table(["bondid", "ip", "token"], quiet=args.q)
            bonds = BondDatabase.get_bonds()
            for bondid in bonds.keys():
                b = bonds[bondid]
                table.add_row(
                    {"bondid": bondid, "ip": b.get("ip"), "token": b.get("token")}
                )
