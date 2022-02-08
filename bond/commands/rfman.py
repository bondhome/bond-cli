import bond.proto
from bond.database import BondDatabase


class RFManCommand(object):
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
        "--bond-id": {"help": "ignore selected Bond and use provided"},
    }

    def run(self, args):
        bondid = args.bond_id or BondDatabase.get_assert_selected_bondid()
        rsp = bond.proto.patch(
            bondid,
            topic="debug/rfman",
            body={"log_signals": args.log_signals, "silence_tx": args.silence_tx},
        )
        body = rsp.get("b", {})
        print(
            f"RF Manager settings: Log Signals ({body.get('log_signals')}) | Silence Transmission ({body.get('silence_tx')})"  # noqa: E501
        )
        if rsp["s"] > 299:
            print(f"HTTP {rsp['s']} {rsp['b']['_error_msg']}")
