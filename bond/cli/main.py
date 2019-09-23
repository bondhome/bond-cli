import importlib
import argparse

_parser = argparse.ArgumentParser(prog='bond')
_subparsers = _parser.add_subparsers(dest='subparser_name',
    help='sub-command help')
_parser.set_defaults(func=lambda x: None)

def load_commands(COMMANDS):
    for COMMAND in COMMANDS:
        command_module = importlib.import_module('bond.commands.' + COMMAND)
        command_module.register()

def register(command):
    name = str(command)
    parser_a = _subparsers.add_parser(name)
    parser_a.set_defaults(func=command.run)
    if hasattr(command, 'arguments'):
        for argument in command.arguments:
            parser_a.add_argument(*argument[0], **argument[1])

def execute_from_command_line(argv):
    args = _parser.parse_args()
    args.func(args)
