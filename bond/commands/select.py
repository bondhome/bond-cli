from .base_command import BaseCommand
from .token import check_unlocked_token
from bond.database import BondDatabase
from ..cli.console import LogLine


class SelectCommand(BaseCommand):
    subcmd = "select"
    help = "Select a single Bond to interact with. If the token of this Bond is unlocked, it will be set. (The easiest way to unlock a token is with a power cycle)"
    arguments = {
        "bond_id": {
            "nargs": "?",
            "help": "Bond ID to interact with in subsequent commands",
        },
        "--none": {"action": "store_true", "help": "clear selection"},
        "--ip": {"help": "specify Bond IP address"},
        "--port": {"help": "specify Bond HTTP port"},
    }

    def run(self, args):
        if args.bond_id:
            BondDatabase.set("selected_bondid", args.bond_id)
            if args.ip:
                BondDatabase.set_bond(args.BONDID, "ip", args.ip)
                LogLine("Set %s IP %s" % (args.BONDID, args.ip))
            if args.port:
                BondDatabase.set_bond(args.BONDID, "port", args.port)
                LogLine("Set %s port %s" % (args.BONDID, args.ip))
            check_unlocked_token()
        if args.none:
            BondDatabase.set("selected_bondid", None)
        LogLine("Selected Bond: %s" % BondDatabase.get("selected_bondid"))


def register():
    SelectCommand()
