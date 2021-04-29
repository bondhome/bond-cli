import sys

import bond.cli

COMMANDS = [
    "discover",
    "select",
    "version",
    "token",
    "list",
    "devices",
    "device_create",
    "livelog",
    "signal",
    "reset",
    "reboot",
    "wifi",
    "upgrade",
    "rfman",
]


def run():
    bond.cli.load_commands(COMMANDS)
    bond.cli.execute_from_command_line(sys.argv)
