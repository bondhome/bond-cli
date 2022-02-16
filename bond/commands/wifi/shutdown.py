import bond.proto
from bond.database import BondDatabase


class WifiShutdownCommand(object):
    subcmd = "shutdown"
    help = "Shutdown WiFi until reboot (requires fw >= v2.11.4)"
    arguments = {
        "--bond-id": {"help": "ignore selected Bond and use provided"},
    }

    def run(self, args):
        bondid = args.bond_id or BondDatabase.get_assert_selected_bondid()
        rsp = bond.proto.patch(
            bondid,
            topic="debug/wifi",
            body={"shutdown": 1},
        )
        if rsp["s"] > 299:
            print(f"HTTP {rsp['s']} {rsp['b']['_error_msg']}")
