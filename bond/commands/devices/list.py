import bond.proto
from bond.cli.table import Table
from bond.database import BondDatabase


class DevicesListCommand(object):
    subcmd = "list"
    help = "List the selected Bond's devices."
    arguments = {
        "--bond-id": {"help": "ignore selected Bond and use provided ID"},
        "-q": {"help": "dont print table outline (quiet mode)", "action": "store_true"},
    }

    def run(self, args):
        bond_id = args.bond_id or BondDatabase.get_assert_selected_bondid()
        dev_ids = bond.proto.get(bond_id, topic="devices").get("b", {})
        if not args.q:
            print(f"Devices on {bond_id}:")
        with Table(["dev_id", "name", "location"], quiet=args.q) as table:
            for dev_id in dev_ids:
                if dev_id.startswith("_"):
                    continue
                dev = bond.proto.get(bond_id, topic=f"devices/{dev_id}").get("b", {})
                table.add_row(
                    {
                        "dev_id": dev_id,
                        "name": dev.get("name"),
                        "location": dev.get("location"),
                    }
                )
