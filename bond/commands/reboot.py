import requests.exceptions

import bond.proto
from bond.database import BondDatabase

from .base_command import BaseCommand


class RebootCommand(BaseCommand):
    subcmd = "reboot"
    help = """Reboot a Bond. No reset is performed."""
    arguments = {"--cold": {"help": "simulate cold boot", "action": "store_true"}}

    def run(self, args):
        bondid = BondDatabase.get_assert_selected_bondid()
        try:
            body = {}
            if args.cold:
                body["type"] = "cold"
            bond.proto.put(bondid, topic="sys/reboot", body=body)
        except requests.exceptions.ReadTimeout:
            print("Connection timed out, as expected.")


def register():
    RebootCommand()
