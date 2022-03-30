from bond.cli.console import lock


class Table(object):
    col_width = 20

    def __init__(self, header, quiet=False):
        lock.acquire()
        self.open = True
        self.header = header
        self.quiet = quiet
        self.print_header()

    def print_tabbed(self, lst):
        separator = "" if self.quiet else "| "

        print("", end=separator)

        for item in lst:
            print(f"{str(item):<{self.col_width}}", end=separator)

        print()

    def print_border(self):
        if not self.quiet:
            print(" " + "-" * ((self.col_width + 1) * len(self.header) + 2))

    def print_header(self):
        if not self.quiet:
            self.print_border()

        self.print_tabbed(self.header)

        if not self.quiet:
            self.print_tabbed(
                [("-" * (self.col_width - 1)) + " " for _h in self.header]
            )

    def add_row(self, row):
        if self.open:
            self.print_tabbed([(row[h] if h in row else "?") for h in self.header])

    def close(self):
        if self.open:
            self.print_border()
            lock.release()
            self.open = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()
