import bond.proto
from bond.database import BondDatabase


class SignalCommand(object):
    subcmd = "signal"
    help = "Transmit a signal. [Bridge only]"
    arguments = {
        "--data": {"help": "The buffer to transmit", "required": True},
        "--bps": {
            "help": "Signal data rate (bits per second)",
            "type": int,
            "default": 40000,
        },
        "--reps": {"help": "The number of reps to transmit", "type": int, "default": 1},
        "--freq": {"help": "signal frequency (kHz)", "type": int, "required": True},
        "--encoding": {"help": "The signal encoding", "default": "cq"},
        "--modulation": {"help": "The signal modulation", "default": "OOK"},
        "--use-scan": {
            "help": "Whether or not to use the most recently-scanned buffer (takes precedence over all other arguments!)",  # noqa: E501
            "action": "store_true",
        },
    }

    def run(self, args):
        bondid = BondDatabase.get_assert_selected_bondid()
        rsp = bond.proto.put(
            bondid,
            topic="signal/tx",
            body={
                "freq": args.freq,
                "data": args.data,
                "bps": args.bps,
                "reps": args.reps,
                "encoding": args.encoding,
                "modulation": args.modulation,
                "use_scan": args.use_scan,
            },
        )
        if rsp["s"] > 299:
            print(f"HTTP {rsp['s']} {rsp['b']['_error_msg']}")
