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
            selected_bond = BondDatabase().get("selected_bondid")
            for bondid in bonds.keys():
                b = bonds[bondid]
                bond_id_display = (
                    bondid + " <-----"
                    if not args.q and bondid == selected_bond
                    else bondid
                )
                table.add_row(
                    {
                        "bondid": bond_id_display,
                        "ip": b.get("ip"),
                        "token": b.get("token"),
                    }
                )
