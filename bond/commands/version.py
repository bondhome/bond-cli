import bond.proto
from bond.commands.base_command import BaseCommand
from bond.database import BondDatabase


class VersionCommand(BaseCommand):
    subcmd = "version"
    help = "Get firmware version and target of the selected Bond."
    arguments = {"--bondid": {"help": "ignore selected Bond and use provided"}}

    def run(self, args):
        bond_id = args.bondid or BondDatabase.get_assert_selected_bondid()
        rsp = bond.proto.get(bond_id, topic="sys/version")
        body = rsp.get("b", {})
        print(bond_id)
        print("Target: %s" % body.get("target"))
        print("Version: %s" % body.get("fw_ver"))


def register():
    VersionCommand()
