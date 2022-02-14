from bond.commands.group_shards import list, create, delete


class GroupShardsCommand(object):
    subcmd = "group-shards"
    help = "Interact with the selected Bond's group shards."
    description = "Warning: may cause inconsistency on device groups!"
    subcommands = [
        list.GroupShardsListCommand(),
        create.GroupShardCreateCommand(),
        delete.GroupShardDeleteCommand(),
    ]
