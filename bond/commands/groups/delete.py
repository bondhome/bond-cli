from requests.exceptions import ConnectTimeout

import bond.proto
from bond.database import BondDatabase


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
        for bond_id in BondDatabase.get_bonds():
            try:
                group_shards = bond.proto.get(bond_id, topic="groups").get("b", {})
                for shard_id in group_shards.keys():
                    if shard_id in args.group_ids:
                        if args.force or input(f"Delete group {shard_id} from {bond_id}? [N/y] ").lower() == "y":
                            bond.proto.delete(bond_id, topic=f"groups/{shard_id}")
                            print(f"{shard_id} group deleted from {bond_id}.")
            except (ConnectTimeout, PermissionError):
                pass
