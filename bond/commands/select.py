from .base_command import BaseCommand
import bond.database
from ..cli.console import LogLine


class SelectCommand(BaseCommand):
    subcmd = "select"
    help = "Select a single Bond to interact with."
    arguments = [
        (
            ["BONDID"],
            {"nargs": "?", "help": "Bond ID to interact with in subsequent commands"},
        ),
        (["--none"], {"action": "store_true", "help": "clear selection"}),
        (["--ip"], {"help": "specify Bond IP address"}),
        (["--port"], {"help": "specify Bond HTTP port"}),
    ]

    def run(self, args):
        if args.BONDID:
            bond.database.set("selected_bondid", args.BONDID)
            if args.ip:
                bond.database.set_bond(args.BONDID, "ip", args.ip)
                LogLine("Set %s IP %s" % (args.BONDID, args.ip))
            if args.port:
                bond.database.set_bond(args.BONDID, "port", args.port)
                LogLine("Set %s port %s" % (args.BONDID, args.ip))
        if args.none:
            bond.database.set("selected_bondid", None)
        LogLine("Selected Bond: %s" % bond.database.get("selected_bondid"))


def register():
    SelectCommand()
