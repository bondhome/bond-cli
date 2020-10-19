from .base_command import BaseCommand
from bond.database import BondDatabase
import bond.proto
import requests.exceptions

class RebootCommand(BaseCommand):
    subcmd = "reboot"
    help = """Reboot a Bond. No reset is performed."""
    arguments = {
    }

    def run(self, args):
        bondid = BondDatabase.get_assert_selected_bondid()
        try:
            bond.proto.put(bondid, topic="sys/reboot", body={})
        except requests.exceptions.ReadTimeout:
            print("Connection timed out, as expected.\nDevice ")

def register():
    RebootCommand()
