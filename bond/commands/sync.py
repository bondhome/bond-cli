import bond.proto
from bond.database import BondDatabase
import json
import os
from pprint import pprint
import threading


def drop_shadow(bondid):
    bond_entry = BondDatabase.get("bonds")[bondid]
    if 'shadow' in bond_entry:
        del bond_entry['shadow']
    BondDatabase.set("bonds", BondDatabase.get("bonds"))


def sync(bondid, verbose=False):
    bond_entry = BondDatabase.get("bonds")[bondid]
    if 'shadow' not in bond_entry:
        bond_entry['shadow'] = {}
    shadow = bond_entry['shadow']

    # returns list of subtopics that have different hashes ('_')
    def update_shadow(topic, body, verbose=False):
        if not verbose:
            print = lambda *args, **kwargs: None
        else:
            print = __builtins__['print']
        d = shadow
        if topic:
            parts = topic.split('/')
            for p in parts:
                d = d.setdefault(p, {})
        rv = []
        # find hashes of children that have changed
        for k, v in body.items():
            # local fields are directly updated
            if k.startswith('_') or not isinstance(v, dict) or '_' not in v:
                d[k] = v
                continue
            # new children are added
            if k not in d:
                print(f"  new:{k}", end='')
                d[k] = v
                rv.append(k)
            # children with changed hashes are updated
            if d[k]['_'] != v['_']:
                d[k]['_'] = v['_']
                rv.append(k)
        # children that have been removed are deleted
        for k in list(d.keys()):
            if k not in body:
                print(f"  del:{k}", end='')
                del d[k]
        print()
        return rv

    def walk(topic):
        topic = topic.strip('/')
        rsp = bond.proto.get(bondid, topic=topic)
        if rsp['s'] >= 300:
            print(f"HTTP {rsp['s']} {topic}")
            return
        body = rsp['b']
        if verbose:
            print(f"GET {topic}...", end='')
        if isinstance(body, dict):
            changed_children = update_shadow(topic, body, verbose=verbose)
            for k in changed_children:
                walk(f"{topic}/{k}")
    walk('')
    BondDatabase.set("bonds", BondDatabase.get("bonds"))


class SyncCommand(object):
    subcmd = "sync"
    help = "Update local database for selected Bond"
    arguments = {
        "--verbose": {
            "help": "Print out all the details of the sync",
            "action": "store_true",
        },
        "--full": {
            "help": "Re-sync everything, not just the delta",
            "action": "store_true",
        },
        "--print": {
            "help": "Print out the shadow after syncing",
            "action": "store_true",
        },
        "--all": {
            "help": "Sync all bonds",
            "action": "store_true",
        },
    }

    def run(self, args):
        if args.all:
            bondids = BondDatabase.get_bonds().keys()
            print(f"Syncing {len(bondids)} bonds...")
        else:
            bondids = [BondDatabase.get_assert_selected_bondid()]

        def worker(bondid):
            if args.full:
                drop_shadow(bondid)
            try:
                sync(bondid, verbose=args.verbose)
                print(f"{bondid} synced.")
            except Exception as e:
                errmsg = str(type(e).__name__)
                print(f"Error syncing {bondid}: {errmsg}")

        threads = []
        for bondid in bondids:
            t = threading.Thread(target=worker, args=(bondid,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        if args.all:
            print("Sync complete.")


