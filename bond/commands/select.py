from .base_command import BaseCommand
import bond.database

class SelectCommand(BaseCommand):
    subcmd = 'select'
    arguments = [
        (
            ['bondid'],
            {'nargs': '?',
             'help': 'Bond ID to interact with in subsequent commands'}
        ),
        (
            ['--none'],
            {'action': 'store_true',
             'help': 'clear selection'}
        )
    ]

    def run(self, args):
        if args.none:
            bond.database.set('selected_bond', None)
        elif args.bondid:
            bond.database.set('selected_bond', args.bondid)
        print("Selected Bond: %s" % bond.database.get('selected_bond'))

def register():
    SelectCommand()
