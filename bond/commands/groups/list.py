import bond.proto
from bond.cli.table import Table


class GroupsListCommand(object):
    subcmd = "list"
    help = "List device groups."

    arguments = {
        "-q": {
            "help": "dont print table outline (quiet mode)",
            "action": "store_true",
        },
    }

    def run(self, args):
        table = Table(["group_id", "bonds"], quiet=args.q)
        groups = {}

        for thread in bond.proto.get_all_async(
            topic="groups",
            on_success=lambda bond_id, response: include_group_shards(
                groups, bond_id, response.get("b", {})
            ),
            on_error=lambda _bond_id, _error_msg: None,
        ):
            thread.join()

        for group_id, bonds in groups.items():
            table.add_row({"group_id": group_id, "bonds": ",".join(bonds)})


def include_group_shards(groups, bond_id, group_shards):
    group_ids = [
        group_id for group_id in group_shards.keys() if not group_id.startswith("_")
    ]
    for group in group_ids:
        groups[group] = groups.get(group, []) + [bond_id]
