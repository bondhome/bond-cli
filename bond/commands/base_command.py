import bond.cli


class BaseCommand(object):
    def __init__(self):
        bond.cli.register(self)

    def __str__(self):
        return self.subcmd
