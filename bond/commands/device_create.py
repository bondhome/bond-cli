from .base_command import BaseCommand
from bond.database import BondDatabase
import bond.proto
from .devices import DevicesCommand


class DeviceCreateCommand(BaseCommand):
    subcmd = "device_create"
    help = "Create a new device. [Bridge only]"
    arguments = {
        "--name": {"help": "device name", "required": True},
        "--template": {"help": "template name (RCF84, A1, etc.)", "required": True},
        "--addr": {"help": "device address (binary)", "required": True},
        "--freq": {"help": "signal frequency (kHz)", "type": int, "required": True},
        "--bps": {
            "help": "signal data rate (bits per second)",
            "type": int,
            "required": True,
        },
        "--zero_gap": {
            "help": "inter-packet space duration (milliseconds)",
            "type": int,
            "required": True,
        },
    }

    def run(self, args):
        bondid = BondDatabase.get_assert_selected_bondid()
        rsp = bond.proto.post(
            bondid,
            topic="devices",
            body={
                "name": args.name,
                "template": args.template,
                "properties": {
                    "addr": args.addr,
                    "freq": args.freq,
                    "bps": args.bps,
                    "zero_gap": args.zero_gap,
                },
            },
        )
        if rsp["s"] > 299:
            print("HTTP %d %s" % (rsp["s"], rsp["b"]["_error_msg"]))
        DevicesCommand().run(None)


def register():
    DeviceCreateCommand()
