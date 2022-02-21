from base64 import b64encode

import bond.proto
from bond.database import BondDatabase


class WifiConnectCommand(object):
    subcmd = "connect"
    help = "Connect to WiFi"
    arguments = {
        "--ssid": {
            "help": "The SSID (name) of the WiFi access point to connect to",
            "required": True,
        },
        "--password": {"help": "The password", "required": True},
        "--bond-id": {"help": "ignore selected Bond and use provided"},
    }

    def run(self, args):
        bondid = args.bond_id or BondDatabase.get_assert_selected_bondid()
        rsp = bond.proto.put(
            bondid,
            topic="sys/wifi/sta",
            body={
                "ssid": b64encode(args.ssid.encode()).decode(),
                "password": b64encode(args.password.encode()).decode(),
            },
        )
        if rsp["s"] > 299:
            print(f"HTTP {rsp['s']} {rsp['b']['_error_msg']}")
