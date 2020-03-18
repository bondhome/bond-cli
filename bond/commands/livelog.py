from .base_command import BaseCommand
from bond.database import BondDatabase
import bond.proto
from .devices import DevicesCommand
import datetime
import socket
import random
import time
import sys
import os

LEVEL_MAP = {"warn": 2, "info": 3, "debug": 4, "trace": 5}


def do_livelog(bondid, ip, port):
    bond.proto.delete(bondid, topic="debug/livelog")
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


class LivelogCommand(BaseCommand):
    subcmd = "livelog"
    help = "Start streaming logs"
    arguments = {
        "--ip": {"help": "IP of log server"},
        "--port": {"help": "UDP port of log server"},
        "--level": {
            "help": "set the verbosity: warn, info, debug (may slow the Bond), or trace (will make the bond unuseably slow, it's recommended to only use this in subys-level)",
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
        "--out": {
            "help": "a filename to write the logs to",
            "default": os.devnull,
        }
    }

    def run(self, args):
        bondid = BondDatabase.get_assert_selected_bondid()

        if args.level:
            bond.proto.patch(
                bondid, topic="debug/syslog", body={"lvl": LEVEL_MAP[args.level]}
            )
        if args.subsys:
            body = {"subsys": args.subsys}
            if args.subsys_level:
                body["lvl"] = LEVEL_MAP[args.subsys_level]
            bond.proto.patch(bondid, topic="debug/syslog", body=body)

        if args.ip is None:
            with open(args.out, "w+") as log:
                my_ip = get_my_ip(BondDatabase.get_bonds()[bondid]["ip"])
                sock, UDP_PORT = listen(my_ip)
                do_livelog(bondid, my_ip, UDP_PORT)
                log.write("\n===== %s =====\n" % datetime.datetime.now())
                while True:
                    data, addr = sock.recvfrom(1024 * 16)
                    logline = data.decode("utf-8")
                    sys.stdout.write(logline)
                    log.write(logline)
                    log.flush()
        else:
            do_livelog(bond, args.ip, int(args.port))


def register():
    LivelogCommand()
