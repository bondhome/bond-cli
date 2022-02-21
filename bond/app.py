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
    "devices_clear",
    "groups",
    "group_create",
    "groups_clear",
    "livelog",
    "signal",
    "reset",
    "reboot",
    "wifi",
    "upgrade",
    "rfman",
    "backup",
]


def run():
    bond.cli.load_commands(COMMANDS)
    bond.cli.execute_from_command_line(sys.argv)
