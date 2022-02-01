import bond.proto
from bond.cli.table import Table
from bond.database import BondDatabase


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
        groups = {}
        for bond_id in BondDatabase.get_bonds():
            try:
                group_shards = bond.proto.get(bond_id, topic="groups").get("b", {})
                for shard_id in group_shards.keys():
                    if shard_id.startswith("_"):
                        continue
                    groups[shard_id] = groups.get(shard_id, []) + [bond_id]
            except Exception:
                pass
        table = Table(["group_id", "bonds"], quiet=args.q)
        for group, bonds in groups.items():
            table.add_row({"group_id": group, "bonds": ",".join(bonds)})
