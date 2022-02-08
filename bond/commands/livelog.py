import datetime
import os
import random
import socket
import sys
import time

from requests.exceptions import RequestException

import bond.proto
from bond.database import BondDatabase

LEVEL_MAP = {"warn": 2, "info": 3, "debug": 4, "trace": 5}


def stop_livelog(bondid):
    bond.proto.delete(bondid, topic="debug/livelog")


def do_livelog(bondid, ip, port):
    stop_livelog(bondid)
    time.sleep(0.5)
    bond.proto.put(bondid, topic="debug/livelog", body={"ip": ip, "port": port})


def get_my_ip(remote_host):
    # determine local host ip by outgoing test to another host
    # use port 9 (discard protocol - RFC 863) over UDP4
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((remote_host, 9))
        my_ip = s.getsockname()[0]
        return my_ip


def listen(my_ip):
    UDP_IP = my_ip
    UDP_PORT = random.randint(30000, 40000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
    sock.bind((UDP_IP, UDP_PORT))
    return sock, UDP_PORT


def auto_int(string: str) -> int:
    """Attempts to automatically detect the base of the input string and parse it as
    an int"""
    return int(string, 0)


class LivelogCommand(object):
    subcmd = "livelog"
    help = "Start streaming logs"
    arguments = {
        "--bond-id": {"help": "ignore selected Bond and use provided"},
        "--ip": {"help": "IP of log server"},
        "--port": {"help": "UDP port of log server"},
        "--level": {
            "help": "set the verbosity: warn, info, debug (may slow the Bond),"
            "or trace (will make the bond unuseably slow, it's recommended to only use this in subys-level)",
            "choices": LEVEL_MAP.keys(),
        },
        "--subsys": {
            "help": "the subsys target to change the log level for",
            "type": auto_int,
        },
        "--subsys-level": {
            "help": "set the verbosity for the given subsys: warn, info, debug, or trace",
            "choices": LEVEL_MAP.keys(),
        },
        "--out": {"help": "a filename to write the logs to", "default": os.devnull},
        "--delete": {  # TODO: refactor to subcommand when possible
            "help": "stop the bond from logging, and restores its default verbosity, improving performance",
            "action": "store_true",
        },
    }

    def run(self, args):  # noqa: C901
        bond_id = args.bond_id or BondDatabase.get_assert_selected_bondid()

        def tear_down_livelog():
            try:
                stop_livelog(bond_id)
                print("Livelog session stopped")
            except RequestException:
                pass
            if args.out != "/dev/null":
                print(f"Logs written to {args.out}")

        if args.delete:
            stop_livelog(bond_id)
            bond.proto.delete(bond_id, topic="debug/syslog")
            print(f"Livelog stopped for {bond_id}")
            return
        if args.level:
            bond.proto.patch(
                bond_id, topic="debug/syslog", body={"lvl": LEVEL_MAP[args.level]}
            )
        if args.subsys:
            body = {"subsys": args.subsys}
            if args.subsys_level:
                body["lvl"] = LEVEL_MAP[args.subsys_level]
            bond.proto.patch(bond_id, topic="debug/syslog", body=body)

        if args.ip:
            do_livelog(bond, args.ip, int(args.port))
        else:
            my_ip = get_my_ip(BondDatabase.get_bonds()[bond_id]["ip"])
            sock, UDP_PORT = listen(my_ip)
            do_livelog(bond_id, my_ip, UDP_PORT)
        with open(args.out, "w+") as log:
            log.write(f"\n===== {datetime.datetime.now()} =====\n")
            while True:
                try:
                    data, addr = sock.recvfrom(1024 * 16)
                    logline = data.decode("utf-8")
                    sys.stdout.write(logline)
                    log.write(logline)
                    log.flush()
                except KeyboardInterrupt:
                    tear_down_livelog()
                    break
