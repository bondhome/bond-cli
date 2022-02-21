import time

from bond.cli.table import Table
from bond.proto.mdns import Scanner


class DiscoverCommand(object):
    subcmd = "discover"
    help = "Discover Bonds on local network."
    arguments = {
        "-q": {"help": "dont print table outline (quiet mode)", "action": "store_true"}
    }

    def run(self, args):
        table = Table(["bondid", "ip", "port"], quiet=args.q)
        scanner = Scanner(table.add_row)  # noqa: F841
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            pass
