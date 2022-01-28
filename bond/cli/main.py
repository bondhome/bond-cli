import argparse

main_parser = argparse.ArgumentParser(prog="bond")
main_subparsers = main_parser.add_subparsers()
main_parser.set_defaults(func=lambda x: main_parser.print_help())


def load_commands(commands):
    for command in commands:
        help_text = command.help if hasattr(command, "help") else None
        cmd_parser = main_subparsers.add_parser(command.subcmd, help=help_text)
        cmd_parser.set_defaults(func=command.run)
        if hasattr(command, "setup"):
            command.setup(cmd_parser)
        if hasattr(command, "arguments"):
            for arg, config in command.arguments.items():
                cmd_parser.add_argument(arg, **config)
        if hasattr(command, "subcommands"):
            subcmd_subparser = cmd_parser.add_subparsers()
            for cmd in command.subcommands:
                subcmd_parser = subcmd_subparser.add_parser(cmd.subcmd)
                subcmd_parser.set_defaults(func=cmd.run)
                if hasattr(cmd, "setup"):
                    cmd.setup(subcmd_parser)
                if hasattr(cmd, "arguments"):
                    for arg, config in cmd.arguments.items():
                        subcmd_parser.add_argument(arg, **config)


def execute_from_command_line(argv):
    args = main_parser.parse_args()
    if args.func:
        args.func(args)
