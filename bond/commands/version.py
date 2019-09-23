from .base_command import BaseCommand
from bond.cli.table import Table
import time

class VersionCommand(BaseCommand):
    subcmd = 'version'

    def run(self, args):
        table = Table(['Bond ID', 'Target', 'Version'])
        time.sleep(5)
        table.close()

def register():
    DiscoverCommand()
