from .base_command import BaseCommand
from bond.database import BondDatabase
import bond.proto
from base64 import b64encode


class WifiCommand(BaseCommand):
    subcmd = "wifi"
    help = "Connect to WiFi"
    arguments = {
        "--ssid": {
            "help": "The SSID (name) of the WiFi access point to connect to",
            "required": True,
        },
        "--password": {"help": "The password", "required": True},
    }

    def run(self, args):
        bondid = BondDatabase.get_assert_selected_bondid()
        rsp = bond.proto.put(
            bondid,
            topic="sys/wifi/sta",
            body={
                "ssid": b64encode(args.ssid.encode()).decode(),
                "password": b64encode(args.password.encode()).decode(),
            },
        )
        if rsp["s"] > 299:
            print("HTTP %d %s" % (rsp["s"], rsp["b"]["_error_msg"]))


def register():
    WifiCommand()
