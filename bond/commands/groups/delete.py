import bond.proto
from bond.database import BondDatabase


class GroupDeleteCommand(object):
    subcmd = "delete"
    help = "Delete Bond's groups."
    arguments = {
        "--bondid": {"help": "ignore selected Bond and use provided"},
        "--force": {
            "help": "force deletion with no input from user",
            "action": "store_true",
        },
    }

    def setup(self, parser):
        group = parser.add_mutually_exclusive_group()
        group.add_argument("--group_id", help="ID of the group being deleted")
        group.add_argument("--all", help="delete all groups", action="store_true")

    def run(self, args):
        bond_id = args.bondid or BondDatabase.get_assert_selected_bondid()
        if args.all:
            if args.force or input(f"Delete all groups from {bond_id}? [N/y] ").lower() == "y":
                self.delete_all_groups(bond_id)
        elif args.group_id:
            if args.force or input(f"Delete group {args.group_id}? [N/y] ").lower() == "y":
                bond.proto.delete(bond_id, topic=f"groups/{args.group_id}")
                print(f"{args.group_id} group deleted.")

    def delete_all_groups(self, bond_id):
        groups_ids = bond.proto.get(bond_id, topic="groups").get("b", {})
        for group_id in groups_ids:
            if group_id.startswith("_"):
                continue
            bond.proto.delete(bond_id, topic=f"groups/{group_id}")
            print(f"{group_id} group deleted.")
