from .console import lock


class Table(object):
    col_width = 16

    def __init__(self, header):
        lock.acquire()
        self.open = True
        self.header = header
        self.print_header()

    def print_tabbed(self, lst):
        print("|", end="")
        for item in lst:
            print(("%-" + str(self.col_width) + "s|") % str(item), end="")
        print()

    def print_boarder(self):
        print("-" + "-" * ((self.col_width + 1) * len(self.header) - 1) + "-")

    def print_header(self):
        self.print_boarder()
        self.print_tabbed(self.header)
        self.print_tabbed([("-" * self.col_width) for h in self.header])

    def add_row(self, row):
        if self.open:
            self.print_tabbed([(row[h] if h in row else "?") for h in self.header])

    def close(self):
        if self.open:
            self.print_boarder()
            lock.release()
            self.open = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()
