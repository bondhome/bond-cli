from .base_command import BaseCommand
from .token import update_token
from bond.database import BondDatabase
from ..cli.console import LogLine
from bond.proto import get_async


def update_token_callback(bondid, rsp):
    token = rsp.get("b", {}).get("token")
    if token:
        print(f"{bondid}'s token is unlocked, updating...")
        update_token(token)


class SelectCommand(BaseCommand):
    subcmd = "select"
    help = "Select a single Bond to interact with. If the token of this Bond is unlocked, it will be set. (The easiest way to unlock a token is with a power cycle)"
    arguments = {
        "BONDID": {
            "nargs": "?",
            "help": "Bond ID to interact with in subsequent commands",
        },
        "--none": {"action": "store_true", "help": "clear selection"},
        "--ip": {"help": "specify Bond IP address"},
        "--port": {"help": "specify Bond HTTP port"},
    }

    def run(self, args):
        if args.BONDID:
            BondDatabase.set("selected_bondid", args.BONDID)
            if args.ip:
                BondDatabase.set_bond(args.BONDID, "ip", args.ip)
                LogLine("Set %s IP %s" % (args.BONDID, args.ip))
            if args.port:
                BondDatabase.set_bond(args.BONDID, "port", args.port)
                LogLine("Set %s port %s" % (args.BONDID, args.ip))
            threads = get_async(
                args.BONDID, topic="token", on_success=update_token_callback
            )

        if args.none:
            BondDatabase.set("selected_bondid", None)
        LogLine("Selected Bond: %s" % BondDatabase.get("selected_bondid"))


def register():
    SelectCommand()
