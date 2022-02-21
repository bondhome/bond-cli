import bond.proto
from bond.database import BondDatabase


class ResetCommand(object):
    subcmd = "reset"
    help = """Reset a Bond to set it up again on WiFi, clear its database, or
              reset its firmware to a rescue image"""
    arguments = {
        "type": {
            "help": """setup: clear the WiFi database record, making the Bond
                       disconnect from WiFi and allowing it to be set up again\n
                       factory: clear the Bond's entire database\n
                       rescue: clear the Bond's entire database and restore the original
                       firmware version that the unit shipped with.
                       This is NOT RECOMMENDED unless you really
                       know what you're doing! You probably don't need this unless
                       you're developing firmware for the Bond.""",
            "choices": ["setup", "factory", "rescue"],
        },
        "--bond-id": {"help": "ignore selected Bond and use provided"},
    }

    def run(self, args):
        bondid = args.bond_id or BondDatabase.get_assert_selected_bondid()
        bond.proto.put(bondid, topic="sys/reset", body={"type": args.type})
        # TODO: a response is not expected. When this is fixed in the firmware,
        # check for a success status here
