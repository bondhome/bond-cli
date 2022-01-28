from bond.commands.groups import list, create, delete


class GroupsCommand(object):
    subcmd = "groups"
    help = "Interact with the selected Bond's groups."
    subcommands = [list.GroupsListCommand(), create.GroupCreateCommand(), delete.GroupDeleteCommand()]

    def run(self, args):
        pass