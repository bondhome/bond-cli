import bond.proto
from bond.database import BondDatabase


class GroupDeleteCommand(object):
    subcmd = "delete"
    help = "Delete Bond's groups."
    arguments = {
        "group_ids": {"help": "ID of the group(s) being deleted", "nargs": "*"},
        "--all": {"help": "delete all groups", "action": "store_true"},
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
                or input(f"Delete all groups from {bond_id}? [N/y] ").lower() == "y"
            ):
                self.delete_all_groups(bond_id)
        elif args.group_ids:
            if (
                args.force
                or input(f"Delete group(s) {', '.join(args.group_ids)}? [N/y] ").lower() == "y"
            ):
                for group_id in args.group_ids:
                    bond.proto.delete(bond_id, topic=f"groups/{group_id}")
                    print(f"{group_id} group deleted.")
        else:
            self.parser.print_help()

    def delete_all_groups(self, bond_id):
        groups_ids = bond.proto.get(bond_id, topic="groups").get("b", {})
        for group_id in groups_ids:
            if group_id.startswith("_"):
                continue
            bond.proto.delete(bond_id, topic=f"groups/{group_id}")
            print(f"{group_id} group deleted.")
