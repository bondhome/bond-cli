from .base_command import BaseCommand
from bond.database import BondDatabase
import bond.proto


class RFManCommand(BaseCommand):
    subcmd = "rfman"
    help = "Configure the RF Manager [Bridge Only]"
    arguments = {
        "--silence-tx": {
            "help": "Stop all transmissions from the Bond Bridge (for debugging purposes)",
            "action": "store_true",
        },
        "--log-signals": {
            "help": "Log all signals transmitted by the Bond on BPUP and MQTT transports",
            "action": "store_true",
        },
    }

    def run(self, args):
        bondid = BondDatabase.get_assert_selected_bondid()
        rsp = bond.proto.patch(
            bondid,
            topic="debug/rfman",
            body={"log_signals": args.log_signals, "silence_tx": args.silence_tx},
        )
        body = rsp.get("b", {})
        print(
            "RF Manager settings: Log Signals (%s) | Silence Transmission (%s)"
            % (body.get("log_signals"), body.get("silence_tx"))
        )
        if rsp["s"] > 299:
            print("HTTP %d %s" % (rsp["s"], rsp["b"]["_error_msg"]))


def register():
    RFManCommand()
