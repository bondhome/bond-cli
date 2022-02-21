from bond.commands.groups import list, create, delete


class GroupsCommand(object):
    subcmd = "groups"
    help = "Interact with device groups."
    subcommands = [
        list.GroupsListCommand(),
        create.GroupCreateCommand(),
        delete.GroupDeleteCommand(),
    ]
