import bond.cli
import sys
import bond.database

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
]


def run():
    bond.database.load()
    bond.cli.load_commands(COMMANDS)
    bond.cli.execute_from_command_line(sys.argv)
