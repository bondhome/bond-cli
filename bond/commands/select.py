from .base_command import BaseCommand
import bond.database
from ..cli.console import Logline

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
        ),
        (
            ['--ip'],
            {'help': 'specify Bond IP address'}
        ),
        (
            ['--port'],
            {'help': 'specify Bond HTTP port'}
        ),
    ]

    def run(self, args):
        if args.bondid:
            bond.database.set('selected_bondid', args.bondid)
            if args.ip:
                bond.database.set_bond(args.bondid, 'ip', args.ip)
                Logline("Set %s IP %s" % (args.bondid, args.ip))
            if args.port:
                bond.database.set_bond(args.bondid, 'port', args.port)
                Logline("Set %s port %s" % (args.bondid, args.ip))
        if args.none:
            bond.database.set('selected_bondid', None)
        Logline("Selected Bond: %s" % bond.database.get('selected_bondid'))

def register():
    SelectCommand()
