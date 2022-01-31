import bond.proto
from bond.database import BondDatabase


class DeviceDeleteCommand(object):
    subcmd = "delete"
    help = "Delete Bond's devices."
    arguments = {
        "device_ids": {"help": "ID of the device(s) being deleted", "nargs": "*"},
        "--all": {"help": "delete all devices", "action": "store_true"},
        "--bond-id": {"help": "ignore selected Bond and use provided"},
        "--force": {
            "help": "force deletion with no input from user",
            "action": "store_true",
        },
    }

    def setup(self, parser):
        self.parser = parser

    def run(self, args):
        bond_id = args.bond_id or BondDatabase.get_assert_selected_bondid()
        if args.all:
            if (
                args.force
                or input(f"Delete all devices from {bond_id}? [N/y] ").lower() == "y"
            ):
                self.delete_all_devices(bond_id)
        elif args.device_ids:
            if (
                args.force
                or input(f"Delete device(s) {', '.join(args.device_ids)}? [N/y] ").lower() == "y"
            ):
                for dev_id in args.device_ids:
                    bond.proto.delete(bond_id, topic=f"devices/{dev_id}")
                    print(f"{dev_id} device deleted.")
        else:
            self.parser.print_help()

    def delete_all_devices(self, bond_id):
        dev_ids = bond.proto.get(bond_id, topic="devices").get("b", {})
        for dev_id in dev_ids:
            if dev_id.startswith("_"):
                continue
            bond.proto.delete(bond_id, topic=f"devices/{dev_id}")
            print(f"{dev_id} device deleted.")
