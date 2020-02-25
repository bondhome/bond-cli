from .base_command import BaseCommand
from bond.cli.table import Table
from bond.cli.console import ExceptionLine
import time
from bond.proto import get_all_async, get_async


class DevicesCommand(BaseCommand):
    subcmd = "devices"
    help = "Interact with devices."

    def run(self, args):
        with Table(["bondid", "dev_id", "name", "location"]) as table:

            def chain_devices(bondid, rsp):
                threads = []
                for dev_id in rsp["b"]:
                    if dev_id[:1] == "_":
                        continue
                    threads.append(
                        get_async(
                            bondid,
                            topic="devices/%s" % dev_id,
                            on_success=(
                                lambda dev_id: lambda bondid, rsp: table.add_row(
                                    {
                                        "bondid": bondid,
                                        "dev_id": dev_id,
                                        "name": rsp["b"]["name"],
                                        "location": rsp["b"]["location"],
                                    }
                                )
                            )(dev_id),
                            on_error=(
                                lambda dev_id: lambda bondid, e: [
                                    table.add_row({"bondid": bondid, "dev_id": dev_id}),
                                    ExceptionLine(e),
                                ]
                            )(dev_id),
                        )
                    )
                [t.join() for t in threads]

            threads = get_all_async(
                topic="devices",
                on_success=chain_devices,
                on_error=lambda bondid, e: [
                    table.add_row({"bondid": bondid}),
                    ExceptionLine(e),
                ],
            )
            [t.join() for t in threads]


def register():
    DevicesCommand()
