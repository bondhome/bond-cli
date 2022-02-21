import bond.proto
from bond.database import BondDatabase


class VersionCommand(object):
    subcmd = "version"
    help = "Get firmware version and target of the selected Bond."
    arguments = {"--bond-id": {"help": "ignore selected Bond and use provided"}}

    def run(self, args):
        bond_id = args.bond_id or BondDatabase.get_assert_selected_bondid()
        rsp = bond.proto.get(bond_id, topic="sys/version")
        body = rsp.get("b", {})
        print(bond_id)
        print(f"Target: {body.get('target')}")
        print(f"Version: {body.get('fw_ver')}")
