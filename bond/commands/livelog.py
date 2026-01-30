import datetime
import os
import random
import socket
import sys
import time
import hashlib
import base64
import zlib
from Crypto.Cipher import AES

from requests.exceptions import RequestException

import bond.proto
from bond.database import BondDatabase

LEVEL_MAP = {"warn": 2, "info": 3, "debug": 4, "trace": 5}


def pkcs7_unpad(data: bytes) -> bytes:
    """Remove PKCS7 padding from data."""
    padding_len = data[-1]
    if padding_len < 1 or padding_len > AES.block_size:
        raise ValueError("Invalid PKCS7 padding length.")
    return data[:-padding_len]


def stop_livelog(bondid):
    bond.proto.delete(bondid, topic="debug/livelog")


def do_livelog(bondid, ip, port, key):
    """Tells the Bond to start sending logs to <ip>:<port>."""
    stop_livelog(bondid)
    time.sleep(0.5)
    rsp = bond.proto.put(bondid, topic="debug/livelog", body={"ip": ip, "port": port, "key": key})
    if rsp['s'] == 400:
        if rsp['b']['_error_id'] == 1104:
            raise Exception("Encryption key is required by this Bond. Provide with --key option.")


def get_my_ip(remote_host):
    """
    Determine local IP by opening a UDP socket to a known remote host
    (using port 9, "discard protocol").
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((remote_host, 9))
        my_ip = s.getsockname()[0]
    return my_ip


def listen(my_ip):
    """
    Bind a random high UDP port on the specified IP and return the socket + port.
    """
    UDP_IP = my_ip
    UDP_PORT = random.randint(30000, 40000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    return sock, UDP_PORT


def auto_int(string: str) -> int:
    """Attempts to automatically detect the base of the input string and parse it as an int."""
    return int(string, 0)


class LivelogCommand(object):
    subcmd = "livelog"
    help = "Start streaming logs"
    arguments = {
        "--bond-id": {"help": "Ignore selected Bond and use provided"},
        "--ip": {"help": "IP of the log server (listen mode is used if omitted)"},
        "--port": {"help": "UDP port of the log server (valid if --ip is set)"},
        "--level": {
            "help": (
                "Set the verbosity: warn, info, debug (may slow the Bond), "
                "or trace (will make the Bond unusably slow, recommended only with subsys-level)."
            ),
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
        "--out": {"help": "filename to write the logs to", "default": os.devnull},
        "--delete": {
            "help": "stop the bond from logging and restore default verbosity",
            "action": "store_true",
        },
        "--key": {
            "help": "Encryption key to use for this session (8+ characters, required on v4.12+ firmware)",
            "default": None,
        },
    }

    def run(self, args):
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
            # Stop logging and restore default verbosity
            stop_livelog(bond_id)
            bond.proto.delete(bond_id, topic="debug/syslog")
            print(f"Livelog stopped for {bond_id}")
            return

        # Handle log-level changes
        if args.level:
            bond.proto.patch(
                bond_id, topic="debug/syslog", body={"lvl": LEVEL_MAP[args.level]}
            )
        if args.subsys:
            body = {"subsys": args.subsys}
            if args.subsys_level:
                body["lvl"] = LEVEL_MAP[args.subsys_level]
            bond.proto.patch(bond_id, topic="debug/syslog", body=body)

        # If user explicitly supplied IP/port, we won't listen ourselves
        if args.ip:
            do_livelog(bond_id, args.ip, int(args.port))
            print(f"Livelog directed to {args.ip}:{args.port}")
            return

        # Otherwise, we spin up a local UDP server to receive logs
        my_ip = get_my_ip(BondDatabase.get_bonds()[bond_id]["ip"])
        sock, UDP_PORT = listen(my_ip)
        do_livelog(bond_id, my_ip, UDP_PORT, args.key)
        print(f"Listening for live logs on udp://{my_ip}:{UDP_PORT}")

        # Prepare AES if key is given
        aes_cipher = None
        if args.key:
            hash_output = hashlib.sha256(args.key.encode()).digest()
            # Use first 16 bytes for AES-128
            aes_key = hash_output[:16]
            aes_cipher = AES.new(aes_key, AES.MODE_ECB)  # re-created as needed

        with open(args.out, "w+") as log_file:
            log_file.write(f"\n===== {datetime.datetime.now()} =====\n")

            while True:
                try:
                    data, addr = sock.recvfrom(65535)

                    if not aes_cipher:
                        # No encryption key: log plaintext
                        logline = data.decode("utf-8", errors="replace")
                    else:
                        # Encrypted data expected in format: bondid:CRC32:BASE64_ENCRYPTED_DATA
                        try:
                            data_str = data.decode("utf-8", errors="ignore")
                            parts = data_str.split(":", 2)
                            if len(parts) < 3:
                                raise ValueError("Invalid data format (missing parts).")

                            parsed_bondid = parts[0]
                            crc32_str = parts[1]
                            enc_b64_str = parts[2].strip().replace("\n", "").replace("\r", "")

                            encrypted_bytes = base64.b64decode(enc_b64_str)
                            if len(encrypted_bytes) % AES.block_size != 0:
                                raise ValueError(
                                    "Encrypted data length not multiple of AES block size."
                                )

                            # Decrypt
                            decrypted_data = aes_cipher.decrypt(encrypted_bytes)
                            # Remove PKCS7 padding
                            decrypted_data = pkcs7_unpad(decrypted_data)

                            # Verify CRC32
                            computed_crc32 = zlib.crc32(decrypted_data) & 0xFFFFFFFF
                            computed_crc32_str = "{:08X}".format(computed_crc32)
                            if computed_crc32_str != crc32_str.upper():
                                raise ValueError("CRC32 mismatch.")

                            # Final message in UTF-8
                            message = decrypted_data.decode("utf-8", errors="replace").strip()

                            # Reconstruct a logline for printing/logging
                            logline = f"{parsed_bondid}:{message}\n"

                        except Exception as e:
                            # If decryption fails, log an error
                            logline = f"[Decrypt Error] {addr[0]}:{addr[1]} => {e}\n"

                    sys.stdout.write(logline)
                    log_file.write(logline)
                    log_file.flush()

                except KeyboardInterrupt:
                    tear_down_livelog()
                    break
                except Exception as e:
                    # Catch any other unexpected errors, continue
                    err_msg = f"[Error receiving data] {e}\n"
                    sys.stdout.write(err_msg)
                    log_file.write(err_msg)
                    log_file.flush()
