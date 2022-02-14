import bond.proto
from bond.database import BondDatabase


class GroupShardCreateCommand(object):
    subcmd = "create"
    help = "Create a new group shard."
    arguments = {
        "--name": {"help": "group name", "required": True},
        "--device-ids": {"help": "included devices", "required": True, "nargs": "*"},
        "--group-id": {"help": "predefine group ID (optional)", "required": False},
        "--bond-id": {"help": "ignore selected Bond and use provided"},
    }

    def run(self, args):
        bond_id = args.bond_id or BondDatabase.get_assert_selected_bondid()
        create_group_body = {
            "name": args.name,
            "devices": args.device_ids,
        }

        if args.group_id:
            create_group_body["_id"] = args.group_id

        rsp = bond.proto.post(
            bond_id,
            topic="groups",
            body=create_group_body,
        )
        if rsp["s"] > 299:
            print(f"HTTP {rsp['s']} {rsp['b']['_error_msg']}")
        else:
            print(f"{rsp['b']['_id']} group shard created.")
