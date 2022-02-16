import sys

from bond.cli.main import load_commands, execute_from_command_line
from bond.commands.backup import BackupCommand, RestoreCommand
from bond.commands.devices import DevicesCommand
from bond.commands.discover import DiscoverCommand
from bond.commands.groups import GroupsCommand
from bond.commands.list import BondListCommand
from bond.commands.livelog import LivelogCommand
from bond.commands.reboot import RebootCommand
from bond.commands.reset import ResetCommand
from bond.commands.rfman import RFManCommand
from bond.commands.select import SelectCommand
from bond.commands.signal import SignalCommand
from bond.commands.token import TokenCommand
from bond.commands.upgrade import UpgradeCommand
from bond.commands.version import VersionCommand
from bond.commands.wifi import WifiCommand

COMMANDS = [
    DiscoverCommand(),
    SelectCommand(),
    VersionCommand(),
    TokenCommand(),
    BondListCommand(),
    DevicesCommand(),
    GroupsCommand(),
    LivelogCommand(),
    SignalCommand(),
    ResetCommand(),
    RebootCommand(),
    WifiCommand(),
    UpgradeCommand(),
    RFManCommand(),
    BackupCommand(),
    RestoreCommand(),
]


def run():
    load_commands(COMMANDS)
    execute_from_command_line(sys.argv)
