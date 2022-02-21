import bond.proto
from bond.commands.base_command import BaseCommand
from bond.database import BondDatabase


class GroupCreateCommand(BaseCommand):
    subcmd = "group_create"
    help = "Create a new group."
    arguments = {
        "--name": {"help": "group name", "required": True},
        "--devices": {"help": "included devices", "required": True},
        "--groupid": {"help": "group ID (optional)", "required": False},
        "--bondid": {"help": "ignore selected Bond and use provided"},
    }

    def run(self, args):
        bond_id = args.bondid or BondDatabase.get_assert_selected_bondid()
        create_group_body = {
            "name": args.name,
            "devices": args.devices.split(","),
        }

        if args.groupid:
            create_group_body["_id"] = args.groupid

        rsp = bond.proto.post(
            bond_id,
            topic="groups",
            body=create_group_body,
        )
        if rsp["s"] > 299:
            print("HTTP %d %s" % (rsp["s"], rsp["b"]["_error_msg"]))


def register():
    GroupCreateCommand()
