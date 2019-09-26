from .base_command import BaseCommand
import bond.database
import bond.proto
from .devices import DevicesCommand
import datetime
import socket
import random
import time
import sys


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
        (["--warn"], {"help": "set verbosity to WARN", "action": "store_true"}),
        (["--info"], {"help": "set verbosity to INFO", "action": "store_true"}),
        (
            ["--debug"],
            {
                "help": "set verbosity to DEBUG (may slow the Bond)",
                "action": "store_true",
            },
        ),
    ]

    def run(self, args):
        bondid = bond.database.get_assert_selected_bondid()

        log_fn = bondid + ".livelog"

        if args.warn or args.info or args.debug:
            if args.warn:
                lvl = 2
            if args.info:
                lvl = 3
            if args.debug:
                lvl = 4
            bond.proto.patch(bondid, topic="debug/syslog", body={"lvl": lvl})

        if args.ip is None:
            with open(log_fn, "w+") as log:
                my_ip = get_my_ip(bond.database.get_bonds()[bondid]["ip"])
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
