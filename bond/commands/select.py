from .base_command import BaseCommand
from .token import check_unlocked_token
from bond.database import BondDatabase
from ..cli.console import LogLine


class SelectCommand(BaseCommand):
    subcmd = "select"
    help = """Select a single Bond to interact with,
              If the token of this Bond is unlocked, it will be set.
              (The easiest way to unlock a token is with a power cycle)"""
    arguments = {
        "bond_id": {
            "nargs": "?",
            "help": """Bond ID to interact with in subsequent commands
                       (you can also use a prefix, if it uniquely identifies an
                       already-discovered Bond""",
        },
        "--clear": {"action": "store_true", "help": "clear selection"},
        "--ip": {"help": "specify Bond IP address"},
        "--port": {"help": "specify Bond HTTP port"},
    }

    def run(self, args):
        if args.bond_id:
            matches = [
                bond
                for bond in BondDatabase.get_bonds()
                if bond.lower().startswith(args.bond_id.lower())
            ]
            if len(matches) == 0:
                proceed = input(
                    "%s hasn't been discovered by bond-cli ('bond discover'). Proceed with setting it? It may not be reachable. y/N"
                    % args.bond_id
                )
                if proceed.lower() == "y":
                    bond_id = args.bond_id
                else:
                    raise SystemExit(
                        "Aborting. Try 'bond discover' on the same network as your Bond"
                    )
            if len(matches) == 1:
                bond_id = matches[0]
            if len(matches) > 1:
                print("Ambiguous Bond ID prefix. Potential matches:")
                for match in matches:
                    print(match)
                exit(1)
            BondDatabase.set("selected_bondid", bond_id)
            if args.ip:
                BondDatabase.set_bond(bond_id, "ip", args.ip)
                print("Set %s IP %s" % (bond_id, args.ip))
            if args.port:
                BondDatabase.set_bond(bond_id, "port", args.port)
                print("Set %s port %s" % (bond_id, args.ip))
            print("Selected Bond: %s" % BondDatabase().get("selected_bondid"))
            token = check_unlocked_token()
        elif args.clear:
            BondDatabase().pop("selected_bondid", None)
            print("Cleared selected Bond")


def register():
    SelectCommand()
