import bond.proto
from bond.commands.base_command import BaseCommand
from bond.database import BondDatabase


class DevicesClearCommand(BaseCommand):
    subcmd = "devices_clear"
    help = "Remove all Bond's devices."
    arguments = {
        "--bondid": {"help": "ignore selected Bond and use provided"},
        "--deviceid": {"help": "delete single device"},
        "--force": {
            "help": "force deletion with no input from user",
            "action": "store_true",
        },
    }

    def run(self, args):
        bond_id = args.bondid or BondDatabase.get_assert_selected_bondid()
        dev_ids = bond.proto.get(bond_id, topic="devices").get("b", {})
        dev_ids.pop("_", None)
        for dev_id in dev_ids:
            if args.deviceid and not args.deviceid == dev_id:
                continue
            if args.force or input(f"Delete device {dev_id}? [N/y] ").lower() == "y":
                bond.proto.delete(bond_id, topic="devices/%s" % dev_id)
                print(dev_id + " device deleted (" + bond_id + ")")


def register():
    DevicesClearCommand()
