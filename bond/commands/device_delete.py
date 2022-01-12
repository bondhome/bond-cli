import bond.proto
from bond.database import BondDatabase

from .base_command import BaseCommand
from .devices import DevicesCommand


class DeviceDeleteCommand(BaseCommand):
    subcmd = "device_delete"
    help = "Delete a device. [Bridge only]"
    arguments = {
        "--id": {"help": "device id", "required": True},
    }

    def run(self, args):
        bondid = BondDatabase.get_assert_selected_bondid()
        rsp = bond.proto.delete(
            bondid,
            topic=f"devices/{args.id}",
            body={},
        )
        if rsp["s"] > 299:
            print("HTTP %d %s" % (rsp["s"], rsp["b"]["_error_msg"]))
        DevicesCommand().run(None)


def register():
    DeviceDeleteCommand()
