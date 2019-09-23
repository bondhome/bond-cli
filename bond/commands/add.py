from .base_command import BaseCommand
import bond.database
from bond.cli.console import Logline

class AddCommand(BaseCommand):
    subcmd = 'add'
    arguments = [
        (
            ['token'],
            {'help': 'Bond local token'}
        ),
    ]

    def run(self, args):
        bondid = bond.database.get_assert_selected_bondid()
        bonds = bond.database.get_bonds()
        if bondid not in bonds.keys():
            bonds[bondid] = dict()
            Logline("Adding new Bond to local database.")
        else:
            Logline("Updating token for existing Bond.")
        bonds[bondid]['token'] = args.token
        bond.database.set('bonds', bonds)

def register():
    AddCommand()
