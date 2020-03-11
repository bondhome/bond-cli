import importlib
import argparse
from .console import console_terminate

_parser = argparse.ArgumentParser(prog="bond")
_subparsers = _parser.add_subparsers(dest="subparser_name")
_parser.set_defaults(func=lambda x: None)


def load_commands(COMMANDS):
    for COMMAND in COMMANDS:
        command_module = importlib.import_module("bond.commands." + COMMAND)
        command_module.register()


def register(command):
    name = str(command)
    help = command.help if hasattr(command, "help") else None
    parser_a = _subparsers.add_parser(name, help=help)
    parser_a.set_defaults(func=command.run)
    if hasattr(command, "arguments"):
        for arg, config in command.arguments.items():
            parser_a.add_argument(arg, **config)


def execute_from_command_line(argv):
    args = _parser.parse_args()
    args.func(args)
