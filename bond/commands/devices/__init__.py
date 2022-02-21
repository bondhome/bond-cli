from bond.commands.devices import create, list, delete


class DevicesCommand(object):
    subcmd = "devices"
    help = "Interact with the selected Bond's devices."
    subcommands = [
        list.DevicesListCommand(),
        create.DeviceCreateCommand(),
        delete.DeviceDeleteCommand(),
    ]
