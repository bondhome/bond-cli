from .base_command import BaseCommand
from bond.database import BondDatabase
import time
import bond.proto
import sys
import requests
import json


def register():
    UpgradeCommand()


def get_branch_string(branch, target):
    if branch in ("alpha", "beta", "master"):
        return f"{branch}-{target}"
    elif branch == "trunk":
        return "trunk"
    else:
        return branch.replace("/", "-")


def get_latest_version(target, branch):
    url = f"https://s3.amazonaws.com/bond-updates/v2/{target}/{branch}/versions_internal.json"
    rsp = requests.get(url)
    if rsp.status_code != 200:
        print("Failed to find an upgrade for target %s on branch %s" % (target, branch))
        exit(1)
    return json.loads(rsp.content)["versions"][0]


def do_upgrade(bondid, version_obj):
    bond.proto.delete(bondid, topic="sys/upgrade")
    time.sleep(0.5)
    version_obj["port"] = "443"
    version_obj["http_port"] = "80"
    try:
        bond.proto.put(bondid, topic="sys/upgrade", body=version_obj)
    except:
        # TODO: when this ^ succeeds in starting an upgrade, it shouldn't be timing out
        # and raising an exception... and yet it is.
        pass
    for _ in range(120):
        time.sleep(1)
        try:
            rsp = bond.proto.get(bondid, topic="sys/upgrade")
        except requests.exceptions.ReadTimeout:
            sys.stdout.write(".")
            sys.stdout.flush()
            continue
        progress = rsp["b"]["progress"]
        print(f"Progress: {progress / 10}%")
        if rsp["s"] == 204 or progress == 1000:
            print("Upgrade installed.")
            break
    else:
        raise Exception("Download timeout")
    print("Rebooting...")
    try:
        bond.proto.put(bondid, topic="sys/reboot", timeout=0.5)
    except:
        pass
    for _ in range(120):
        time.sleep(1)

        # check for in progress return get on upgrade
        try:
            rsp = bond.proto.get(bondid, topic="sys/version", timeout=2)
        except requests.exceptions.ConnectTimeout:
            sys.stdout.write(".")
            sys.stdout.flush()
            continue
        print("Reconnected!")
        break
    else:
        raise Exception("Download timeout")

    print(f"Your Bond is now on version {rsp['b']['fw_ver']}!")


class UpgradeCommand(BaseCommand):
    subcmd = "upgrade"
    help = "Upgrade your Bond. Choose either a released firmware or a firmware from a specific branch"
    arguments = {
        "branch": {
            "help": "The branch. Release branches are 'trunk', 'alpha', 'beta', and 'master'. "
            "'master' is the version distributed by the mobile apps in the app stores, "
            "'alpha' and 'trunk' are for internal development use, and may be unstable."
        },
        "--target": {
            "help": "override detected target. Useful in development, but may cause irreversible device malfunction!"
        },
    }

    def run(self, args):
        bondid = BondDatabase.get_assert_selected_bondid()
        print("Connecting to BOND...")
        sys_version = bond.proto.get(bondid, topic="sys/version")["b"]
        target = sys_version["target"]
        current_ver = sys_version["fw_ver"]
        print(f"Detected Target: \t{target}")
        if args.target:
            print(f"Requested Target: \t{args.target}")
            if args.target != target:
                print("Detected and requested targets do not match!")
                print(
                    "WARNING: Continuing may cause irreversible device damage or even a fire hazard."
                )
                response = input(
                    "Are you sure you know EXACTLY what you're doing? [N/yessir] "
                )
                if response != "yessir":
                    print("Yeah, best not to override the target anyways.")
                    exit(1)
                if input("Have your fire extinguisher ready? [N/y]").lower() != "y":
                    print("Well, go find one!")
                    exit(1)
                target = args.target
                print("Target manually overriden.")

        branch = get_branch_string(args.branch, target)
        print(f"Selected Branch: \t{branch}")
        print(f"Current Version: \t{current_ver}")
        version_obj = get_latest_version(target, branch)
        new_ver = version_obj["version"]
        print(f"Installing Version: \t{new_ver}")
        if new_ver == current_ver:
            print("WARNING: Versions are identical.")
        if input("Are you sure? [N/y] ").lower() != "y":
            print("Pfew. That was close. Aborting!")
            exit(1)
        print("Requesting upgrade...")
        do_upgrade(bondid, version_obj)
