from .base_command import BaseCommand
from bond.cli.table import Table
from bond.proto.mdns import Scanner
import time


class DiscoverCommand(BaseCommand):
    subcmd = "discover"
    help = "Discover Bonds on local network."

    def run(self, args):
        table = Table(["bondid", "ip", "port"])
        scanner = Scanner(table.add_row)
        time.sleep(5)


def register():
    DiscoverCommand()
