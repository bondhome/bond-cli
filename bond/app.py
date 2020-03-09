import bond.cli
import sys

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
    "wifi",
]


def run():
    bond.cli.load_commands(COMMANDS)
    bond.cli.execute_from_command_line(sys.argv)
