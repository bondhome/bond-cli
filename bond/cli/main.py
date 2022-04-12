import argparse

main_parser = argparse.ArgumentParser(prog="bond")
main_subparsers = main_parser.add_subparsers()
main_parser.set_defaults(func=lambda _: main_parser.print_help())


def load_commands(commands):
    for command in commands:
        setup_command(command, main_subparsers)


def setup_command(command, subparsers):
    help_text = command.help if hasattr(command, "help") else None
    description_text = command.description if hasattr(command, "description") else None
    cmd_parser = subparsers.add_parser(command.subcmd, help=help_text, description=description_text)

    if hasattr(command, "run"):
        cmd_parser.set_defaults(func=command.run)
    else:
        cmd_parser.set_defaults(func=lambda _: cmd_parser.print_help())

    if hasattr(command, "setup"):
        command.setup(cmd_parser)

    if hasattr(command, "arguments"):
        for arg, config in command.arguments.items():
            cmd_parser.add_argument(arg, **config)

    if hasattr(command, "subcommands"):
        subcmd_subparser = cmd_parser.add_subparsers()
        for cmd in command.subcommands:
            setup_command(cmd, subcmd_subparser)


def execute_from_command_line(argv):
    args = main_parser.parse_args()
    if args.func:
        args.func(args)
