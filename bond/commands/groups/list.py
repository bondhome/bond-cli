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
        "--bond-id": {"help": "only list group shards from the specified Bond"},
    }

    def run(self, args):
        if args.bond_id:
            self.run_on_single_bond(args)
        else:
            self.run_on_all_bonds(args)

    def run_on_single_bond(self, args):
        bond_id = args.bond_id
        group_ids = bond.proto.get(bond_id, topic="groups").get("b", {})
        if not args.q:
            print(f"Group shards on {bond_id}:")
        with Table(["group_id", "name", "types", "devices"], quiet=args.q) as table:
            for group_id in group_ids:
                if group_id.startswith("_"):
                    continue
                group = bond.proto.get(bond_id, topic=f"groups/{group_id}").get("b", {})
                table.add_row(
                    {
                        "group_id": group_id,
                        "name": group.get("name"),
                        "types": ",".join(group.get("types", [])),
                        "devices": ",".join(group.get("devices", [])),
                    }
                )

    def run_on_all_bonds(self, args):
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
