from base64 import b64encode

import bond.proto
from bond.database import BondDatabase


class WifiCommand(object):
    subcmd = "wifi"
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


class WifiShutdownCommand(object):
    subcmd = "wifi_shutdown"
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
