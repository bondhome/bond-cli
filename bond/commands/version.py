from .base_command import BaseCommand
from bond.cli.table import Table
import time
from bond.proto import get_all_async


class VersionCommand(BaseCommand):
    subcmd = "version"
    help = "Get firwmare version."

    def run(self, args):
        table = Table(["Bond ID", "Target", "Version"])
        threads = get_all_async(
            topic="sys/version",
            on_success=lambda bondid, rsp: table.add_row(
                {
                    "Bond ID": bondid,
                    "Target": rsp["b"]["target"],
                    "Version": rsp["b"]["fw_ver"],
                }
            ),
            on_error=lambda bondid, e: table.add_row({"Bond ID": bondid}),
        )
        [t.join() for t in threads]


def register():
    VersionCommand()
