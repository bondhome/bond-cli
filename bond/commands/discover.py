import time

from bond.cli.table import Table
from bond.commands.base_command import BaseCommand
from bond.proto.mdns import Scanner


class DiscoverCommand(BaseCommand):
    subcmd = "discover"
    help = "Discover Bonds on local network."

    def run(self, args):
        table = Table(["bondid", "ip", "port"])
        scanner = Scanner(table.add_row)    # noqa: F841
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            pass


def register():
    DiscoverCommand()
