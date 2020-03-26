import time

from .base_command import BaseCommand
from bond.cli.table import Table
from bond.database import BondDatabase
import bond.proto


class DevicesCommand(BaseCommand):
    subcmd = "devices"
    help = "Interact with the selected Bond's devices."

    def run(self, args):
        bond_id = BondDatabase.get_assert_selected_bondid()
        dev_ids = bond.proto.get(bond_id, topic="devices").get("b", {})
        print("Devices on %s" % bond_id)
        with Table(["dev_id", "name", "location"]) as table:
            dev_ids.pop("_", None)
            for dev_id in dev_ids:
                dev = bond.proto.get(bond_id, topic="devices/%s" % dev_id).get("b", {})
                table.add_row(
                    {
                        "dev_id": dev_id,
                        "name": dev.get("name"),
                        "location": dev.get("location"),
                    }
                )


def register():
    DevicesCommand()
