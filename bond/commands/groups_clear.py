import bond.proto
from bond.commands.base_command import BaseCommand
from bond.database import BondDatabase


class GroupsClearCommand(BaseCommand):
    subcmd = "groups_clear"
    help = "Remove all Bond's groups."
    arguments = {
        "--bondid": {"help": "ignore selected Bond and use provided"},
        "--groupid": {"help": "delete single group"},
        "--force": {
            "help": "force deletion with no input from user",
            "action": "store_true",
        },
    }

    def run(self, args):
        bond_id = args.bondid or BondDatabase.get_assert_selected_bondid()

        group_ids = bond.proto.get(bond_id, topic="groups").get("b", {})
        group_ids.pop("_", None)

        for group_id in group_ids:
            if args.groupid and not args.groupid == group_id:
                continue
            if args.force or input(f"Delete group {group_id}? [N/y] ").lower() == "y":
                bond.proto.delete(bond_id, topic="groups/%s" % group_id)
                print(group_id + " group deleted (" + bond_id + ")")


def register():
    GroupsClearCommand()
