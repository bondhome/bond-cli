from .base_command import BaseCommand
from bond.database import BondDatabase
import bond.proto


class ResetCommand(BaseCommand):
    subcmd = "reset"
    help = """Reset a Bond, either to set it back up (setup reset), clear its database 
              completely (factory reset), or clear its database and reset it to
              its original firmware (rescue reset, which is NOT RECOMMENDED UNLESS
              YOU KNOW WHAT YOU'RE DOING!)"""
    arguments = [
        (
            ["type"],
            {
                "help": """setup: clear the WiFi database record, making the Bond
                        disconnect from WiFi and allowing it to be set up again
                        factory: clear the Bond's entire database
                        rescue: clear the Bond's entire database and reset its firmware
                        to factory settings (this is NOT RECOMMENDED unless you really
                        know what you're doing! You probably don't need this unless
                        you're developing firmware for the Bond)""",
                "choices": ["setup", "factory", "rescue"],
            },
        )
    ]

    def run(self, args):
        bondid = BondDatabase.get_assert_selected_bondid()
        bond.proto.put(bondid, topic="sys/reset", body={"type": args.type})
        # TODO: a response is not expected. When this is fixed in the firmware,
        # check for a success status here


def register():
    ResetCommand()
