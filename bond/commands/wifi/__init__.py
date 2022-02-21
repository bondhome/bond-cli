from bond.commands.wifi import connect, shutdown


class WifiCommand(object):
    subcmd = "wifi"
    help = "Interact with Bond's wifi"
    subcommands = [
        connect.WifiConnectCommand(),
        shutdown.WifiShutdownCommand(),
    ]
