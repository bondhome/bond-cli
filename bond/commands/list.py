from .base_command import BaseCommand
import bond.database
from bond.cli.table import Table

class ListCommand(BaseCommand):
    subcmd = 'list'

    def run(self, args):
        table = Table(['Bond ID', 'Token'])
        bonds = bond.database.get_bonds()
        for bondid in bonds.keys():
            table.add_row({
                'Bond ID': bondid,
                'Token': bonds[bondid]['token'],
                })

def register():
    ListCommand()
