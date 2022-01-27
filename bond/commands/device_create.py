import bond.proto
from bond.commands.base_command import BaseCommand
from bond.database import BondDatabase


class DeviceCreateCommand(BaseCommand):
    subcmd = "device_create"
    help = "Create a new device. [Bridge only]"
    arguments = {
        "--name": {"help": "device name", "required": True},
        "--template": {"help": "template name (RCF84, A1, etc.)", "required": True},
        "--location": {
            "help": "location name (Bedroom, Living Room, etc.)",
            "required": True,
        },
        "--addr": {"help": "device address (binary)", "required": False},
        "--freq": {"help": "signal frequency (kHz)", "type": int, "required": False},
        "--bps": {
            "help": "signal data rate (bits per second)",
            "type": int,
            "required": False,
        },
        "--zero_gap": {
            "help": "inter-packet space duration (milliseconds)",
            "type": int,
            "required": False,
        },
        "--bondid": {"help": "ignore selected Bond and use provided"},
    }

    def run(self, args):
        bond_id = args.bondid or BondDatabase.get_assert_selected_bondid()
        properties = {}
        if args.addr:
            properties["addr"] = args.addr
        if args.freq:
            properties["freq"] = args.freq
        if args.bps:
            properties["bps"] = args.bps
        if args.zero_gap:
            properties["zero_gap"] = args.zero_gap
        rsp = bond.proto.post(
            bond_id,
            topic="devices",
            body={
                "name": args.name,
                "location": args.location,
                "template": args.template,
                "properties": properties,
            },
        )
        if rsp["s"] > 299:
            print("HTTP %d %s" % (rsp["s"], rsp["b"]["_error_msg"]))


def register():
    DeviceCreateCommand()
