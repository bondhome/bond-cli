import datetime
import os
import time
import ssl
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from queue import Queue
from threading import Thread

import requests.exceptions

import bond.proto
from bond.database import BondDatabase, DB_DIRNAME

Q = Queue()

class ChunkedRequestHandler(SimpleHTTPRequestHandler):
    def do_PUT(self):
        self.send_response(200)
        self.end_headers()

        path = self.translate_path(self.path)

        if "Content-Length" in self.headers:
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            with open(path, "wb") as out_file:
                out_file.write(body)
        elif "chunked" in self.headers.get("Transfer-Encoding", ""):
            with open(path, "wb") as out_file:
                while True:
                    line = self.rfile.readline().strip()
                    chunk_length = int(line, 16)

                    if chunk_length != 0:
                        chunk = self.rfile.read(chunk_length)
                        out_file.write(chunk)

                    # Each chunk is followed by an additional empty newline
                    # that we have to consume.
                    self.rfile.readline()

                    # Finally, a chunk size of 0 is an end indication
                    if chunk_length == 0:
                        break
        Q.put(path)

    def handle(self):
        if hasattr(self.connection, 'version'):
            ssl_version = self.connection.version()
            print(f"Connected using TLS version: {ssl_version}")
        else:
            print("No TLS connection or non-SSL connection detected.")
        super().handle()

def start_daemon(port, protocol="http"):
    print(f"Starting server on port {port} with protocol {protocol}")
    os.chdir(DB_DIRNAME)
    handler = ChunkedRequestHandler
    print(f"Handler assigned: {handler}")

    if protocol in ["https", "https-insecure"]:
        # Need to add certificate with name cert.pem and key with name key.pem for
        # testing https connection.
        base_dir = os.path.dirname(os.path.abspath(__file__))  # current script directory
        cert_path = os.path.join(base_dir, "cert.pem")
        key_path = os.path.join(base_dir, "key.pem")

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        if protocol == "https-insecure":
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            context.set_ciphers("DEFAULT")
        context.load_cert_chain(certfile=cert_path, keyfile=key_path)

        # HTTPS Server start
        httpd=HTTPServer(('0.0.0.0', port), handler)
        print("Wrapping socket with SSL...")
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        print(f"Serving at https://0.0.0.0:{port}")
        Thread(target=httpd.serve_forever, daemon=True).start()

    else:
        # HTTP Server start
        httpd=HTTPServer(('0.0.0.0', port), handler)
        print(f"Serving at http://0.0.0.0:{port}")
        Thread(target=httpd.serve_forever, daemon=True).start()

def wait_upload(timeout=None):
    return Q.get(timeout=timeout)

class BackupCommand(object):
    subcmd = "backup"
    help = """Backup a Bond"""
    arguments = {
        "--bond-id": {"help": "ignore selected Bond and use provided"},
        "--protocol": {"help": "Choose protocol: http, https, https-insecure", "choices": ["http", "https", "https-insecure"]},
    }

    def run(self, args):
        protocol = args.protocol or "http"
        start_daemon(4444, protocol)
        bondid = args.bond_id or BondDatabase.get_assert_selected_bondid()
        timestamp = str(int(time.time()))
        security_level = 0
        if protocol == "https-insecure":
            security_level = 1
            body = {
                "backup": 1,
                "https_port": "4444",
                "path": "",
                "timestamp": timestamp,
                "security": security_level,
            }
        elif protocol == "https":
            security_level = 2
            body = {
                "backup": 1,
                "https_port": "4444",
                "path": "",
                "timestamp": timestamp,
                "security": security_level,
            }
        else:
            body = {
            "backup": 1,
            "http_port": "4444",
            "path": "",
            "timestamp": timestamp,
            "security": security_level,
        }

        rsp = bond.proto.put(bondid, topic="sys/backup", body=body)
        print(rsp)
        if rsp["s"] != 200:
            raise Exception(
                f"Error HTTP {rsp['s']} starting backup: {rsp['b']['_error_msg']}"
            )
        time.time()
        while True:
            time.sleep(1)
            rsp = bond.proto.get(bondid, topic="sys/backup")
            if rsp["b"]["backup"] == -1:
                raise Exception(f"Backup error: {rsp['b']['error_msg']}")
            if rsp["b"]["backup"] == 2:
                print("Bond reports backup success.")
                break
        path = ""
        while timestamp not in path:
            path = wait_upload(5)
        print("Backup saved in ~/.bond directory")


def get_file_list():
    fns = list(map(str, Path(DB_DIRNAME).glob("**/*.bondbackup")))
    rv = []
    for fn in fns:
        tok = fn.split("_")
        rv.append(
            {
                "file": fn,
                "bondid": tok[0],
                "version": tok[1],
                "timestamp": int(tok[2]),
                "datestr": datetime.datetime.utcfromtimestamp(int(tok[2]))
                .astimezone()
                .strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
    rv.sort(key=lambda x: x["timestamp"], reverse=True)
    return rv


class RestoreCommand(object):
    subcmd = "restore"
    help = """Restore a Bond."""
    arguments = {
        "--list": {
            "help": "list backups available for restore to selected bond",
            "action": "store_true",
        },
        "--file": {
            "help": "filename of backup to restore (must be in ~/.bond/)",
        },
        "--latest": {
            "help": "restore the most recent backup for selected bond",
            "action": "store_true",
        },
        "--no-reboot": {
            "help": "Only for test purposes. May cause unexpected behavior.",
            "action": "store_true",
        },
        "--bond-id": {"help": "ignore selected Bond and use provided",
        },
        "--protocol": {"help": "Choose protocol: http, https, https-insecure", "choices": ["http", "https", "https-insecure"]},
    }

    def run(self, args):  # noqa: C901
        protocol = args.protocol or "http"
        file_list = get_file_list()
        if args.list or not (args.file or args.latest) or len(file_list) == 0:
            if len(file_list) == 0:
                print("No backups found")
            else:
                print(f"Found {len(file_list)} backups:")
                for f in get_file_list():
                    print("  " + f["datestr"] + "   " + f["file"])
            return

        if args.latest:
            if len(file_list) == 0:
                print("No backups found")
                return
            args.file = file_list[-1]["file"]

        start_daemon(4444, protocol)
        bondid = args.bond_id or BondDatabase.get_assert_selected_bondid()
        # timestamp = str(int(time.time()))
        security_level = 0
        if protocol == "https-insecure":
            security_level = 1
            body = {
                "restore": 1,
                "https_port": "4444",
                "path": "",
                "filename": args.file,
                "security": security_level,
            }
        elif protocol == "https":
            security_level = 2
            body = {
                "restore": 1,
                "https_port": "4444",
                "path": "",
                "filename": args.file,
                "security": security_level,
            }
        else:
            body = {
                "restore": 1,
                "http_port": "4444",
                "path": "",
                "filename": args.file,
                "security": security_level,
            }
        rsp = bond.proto.put(bondid, topic="sys/backup", body=body)
        print(rsp)
        if rsp["s"] != 200:
            raise Exception(
                f"Error HTTP {rsp['s']} starting restore: {rsp['b']['_error_msg']}"
            )
        time.time()
        while True:
            time.sleep(1)
            rsp = bond.proto.get(bondid, topic="sys/backup")
            if rsp["b"]["restore"] == -1:
                raise Exception(f"Restore error: {rsp['b']['error_msg']}")
            if rsp["b"]["restore"] == 2:
                print("Bond reports restore success!")
                break
        if args.no_reboot:
            print("Please reboot Bond for restore to take effect.")
            return
        print("Rebooting Bond now...")
        try:
            bond.proto.put(bondid, topic="sys/reboot")
        except requests.exceptions.ReadTimeout:
            pass
