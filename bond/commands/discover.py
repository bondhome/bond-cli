from .base_command import BaseCommand
from bond.cli.table import Table
from bond.proto.mdns import Scanner
import time

class DiscoverCommand(BaseCommand):
    subcmd = 'discover'

    def run(self, args):
        table = Table(['bondid', 'ip'])
        scanner = Scanner(table.add_row)
        time.sleep(5)

def register():
    DiscoverCommand()
