import bond.proto


class GroupDeleteCommand(object):
    subcmd = "delete"
    help = "Delete device group(s)."
    arguments = {
        "group_ids": {"help": "ID of the group(s) being deleted", "nargs": "*"},
        "--all": {"help": "delete all groups", "action": "store_true"},
        "--bond-id": {"help": "only delete group shards from specified Bond (may cause inconsistency!)"},
        "--force": {
            "help": "force deletion with no input from user",
            "action": "store_true",
        },
    }

    def setup(self, parser):
        self.parser = parser

    def run(self, args):
        if args.bond_id:
            self.run_on_single_bond(args)
        else:
            self.run_on_all_bonds(args)

    def run_on_all_bonds(self, args):
        if args.all:
            if args.force or input("Delete ALL groups? [N/y] ").lower() == "y":
                bond.proto.get_all_async(
                    topic="groups",
                    on_success=lambda bond_id, response: delete_groups_from_bond(bond_id, response.get("b", {}).keys()),
                    on_error=lambda _bond_id, _error_msg: None,
                )
        elif args.group_ids:
            if args.force or input(f"Delete group(s) {', '.join(args.group_ids)}? [N/y] ").lower() == "y":
                bond.proto.get_all_async(
                    topic="groups",
                    on_success=lambda bond_id, response: delete_group_if_present(
                        args.group_ids, bond_id, response.get("b", {}).keys()
                    ),
                    on_error=lambda _bond_id, _error_msg: None,
                )
        else:
            self.parser.print_help()

    def run_on_single_bond(self, args):
        if args.all:
            if args.force or input(f"Delete all group shards from {args.bond_id}? [N/y] ").lower() == "y":
                group_ids = bond.proto.get(args.bond_id, topic="groups").get("b", {}).keys()
                delete_groups_from_bond(args.bond_id, group_ids)
        elif args.group_ids:
            confirmation_text = f"Delete group shard(s) {', '.join(args.group_ids)} from {args.bond_id}? [N/y] "
            if args.force or input(confirmation_text).lower() == "y":
                for group_id in args.group_ids:
                    bond.proto.delete(args.bond_id, topic=f"groups/{group_id}")
                    print(f"{group_id} group deleted from {args.bond_id}.")
        else:
            self.parser.print_help()


def delete_groups_from_bond(bond_id, group_ids):
    for group_id in group_ids:
        if group_id.startswith("_"):
            continue
        bond.proto.delete(bond_id, topic=f"groups/{group_id}")
        print(f"{group_id} group deleted from {bond_id}.")


def delete_group_if_present(deleted_group_ids, bond_id, group_shards):
    group_shard_ids = [
        group_id for group_id in group_shards if not group_id.startswith("_")
    ]
    for deleted_group in deleted_group_ids:
        if deleted_group in group_shard_ids:
            bond.proto.delete(bond_id, topic=f"groups/{deleted_group}")
            print(f"{deleted_group} group deleted from {bond_id}.")
