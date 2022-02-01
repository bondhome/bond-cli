import random

import bond.proto


class GroupCreateCommand(object):
    subcmd = "create"
    help = "Create a new group."
    arguments = {
        "devices": {"help": "included devices, in the format BOND_ID:DEVICE_ID", "nargs": "+"},
        "--name": {"help": "group name", "required": True},
        "--group-id": {"help": "predefine group ID (optional)", "required": False},
    }

    def run(self, args):
        devices = {}
        for device in args.devices:
            bond_id, device_id = device.split(":")
            devices[bond_id] = devices.get(bond_id, []) + [device_id]

        create_group_body = {"name": args.name}

        if args.group_id:
            create_group_body["_id"] = args.group_id
        else:
            uid = f"{random.randrange(2 ** 64):016x}"
            create_group_body["_id"] = uid

        for bond_id, device_ids in devices.items():
            create_group_body["devices"] = device_ids
            rsp = bond.proto.post(
                bond_id,
                topic="groups",
                body=create_group_body,
            )
            if rsp["s"] > 299:
                print(f"HTTP {rsp['s']} {rsp['b']['_error_msg']}")
            else:
                print(f"{rsp['b']['_id']} group created in {bond_id}.")
