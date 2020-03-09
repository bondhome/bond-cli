from .base_command import BaseCommand
from bond.database import BondDatabase
import bond.proto
from .devices import DevicesCommand
import datetime
import socket
import random
import time
import sys

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


class LivelogCommand(BaseCommand):
    subcmd = "livelog"
    help = "Start streaming logs"
    arguments = [
        (["--ip"], {"help": "IP of log server"}),
        (["--port"], {"help": "UDP port of log server"}),
        (
            ["--level"],
            {
                "help": "set the verbosity: warn, info, debug (may slow the Bond), or trace (will definitely slow the Bond)",
                "choices": LEVEL_MAP.keys(),
            },
        ),
    ]

    def run(self, args):
        bondid = BondDatabase.get_assert_selected_bondid()

        log_fn = bondid + ".livelog"

        if args.level:
            bond.proto.patch(
                bondid, topic="debug/syslog", body={"lvl": LEVEL_MAP[args.level]}
            )

        if args.ip is None:
            with open(log_fn, "w+") as log:
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
