from .base_command import BaseCommand
from bond.cli.table import Table
import time
import bond.proto
from bond.database import BondDatabase


class VersionCommand(BaseCommand):
    subcmd = "version"
    help = "Get firmware version and target of the selected Bond."

    def run(self, args):
        bond_id = BondDatabase.get_assert_selected_bondid()
        rsp = bond.proto.get(bond_id, topic="sys/version")
        body = rsp.get("b", {})
        print(bond_id)
        print("Target: %s" % body.get("target"))
        print("Version: %s" % body.get("fw_ver"))


def register():
    VersionCommand()
