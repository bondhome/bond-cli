import bond.proto
from bond.database import BondDatabase


class DeviceDeleteCommand(object):
    subcmd = "delete"
    help = "Delete Bond's devices."
    arguments = {
        "--bond-id": {"help": "ignore selected Bond and use provided"},
        "--force": {
            "help": "force deletion with no input from user",
            "action": "store_true",
        },
    }

    def setup(self, parser):
        group = parser.add_mutually_exclusive_group()
        group.add_argument("--device-id", help="ID of the device being deleted")
        group.add_argument("--all", help="delete all devices", action="store_true")

    def run(self, args):
        bond_id = args.bond_id or BondDatabase.get_assert_selected_bondid()
        if args.all:
            if (
                args.force
                or input(f"Delete all devices from {bond_id}? [N/y] ").lower() == "y"
            ):
                self.delete_all_devices(bond_id)
        elif args.device_id:
            if (
                args.force
                or input(f"Delete device {args.device_id}? [N/y] ").lower() == "y"
            ):
                bond.proto.delete(bond_id, topic=f"devices/{args.device_id}")
                print(f"{args.device_id} device deleted.")

    def delete_all_devices(self, bond_id):
        dev_ids = bond.proto.get(bond_id, topic="devices").get("b", {})
        for dev_id in dev_ids:
            if dev_id.startswith("_"):
                continue
            bond.proto.delete(bond_id, topic=f"devices/{dev_id}")
            print(f"{dev_id} device deleted.")
