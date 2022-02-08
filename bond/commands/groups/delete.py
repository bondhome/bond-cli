import bond.proto


class GroupDeleteCommand(object):
    subcmd = "delete"
    help = "Delete device group(s)."
    arguments = {
        "group_ids": {"help": "ID of the group(s) being deleted", "nargs": "+"},
        "--force": {
            "help": "force deletion with no input from user",
            "action": "store_true",
        },
    }

    def run(self, args):
        if (
            args.force
            or input(f"Delete group(s) {', '.join(args.group_ids)}? [N/y] ").lower()
            == "y"
        ):
            bond.proto.get_all_async(
                topic="groups",
                on_success=lambda bond_id, response: delete_group_if_present(
                    args.group_ids, bond_id, response.get("b", {})
                ),
                on_error=lambda _bond_id, _error_msg: None,
            )


def delete_group_if_present(deleted_group_ids, bond_id, group_shards):
    group_shard_ids = [
        group_id for group_id in group_shards.keys() if not group_id.startswith("_")
    ]
    for deleted_group in deleted_group_ids:
        if deleted_group in group_shard_ids:
            bond.proto.delete(bond_id, topic=f"groups/{deleted_group}")
            print(f"{deleted_group} group deleted from {bond_id}.")
