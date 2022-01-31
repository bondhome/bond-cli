import bond.proto
from bond.cli.table import Table
from bond.database import BondDatabase


class GroupsListCommand(object):
    subcmd = "list"
    help = "List the selected Bond's groups."

    arguments = {
        "--bond-id": {"help": "ignore selected Bond and use provided"},
        "-q": {
            "help": "dont print table outline (quiet mode)",
            "action": "store_true",
        },
    }

    def run(self, args):
        bond_id = args.bond_id or BondDatabase.get_assert_selected_bondid()
        group_ids = bond.proto.get(bond_id, topic="groups").get("b", {})
        if not args.q:
            print(f"Groups on {bond_id}:")
        with Table(["group_id", "name", "types", "devices"], quiet=args.q) as table:
            for group_id in group_ids:
                if group_id.startswith("_"):
                    continue
                group = bond.proto.get(bond_id, topic=f"groups/{group_id}").get("b", {})
                table.add_row(
                    {
                        "group_id": group_id,
                        "name": group.get("name"),
                        "types": group.get("types"),
                        "devices": group.get("devices"),
                    }
                )
