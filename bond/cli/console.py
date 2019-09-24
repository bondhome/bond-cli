
class LogLine(object):
    def __init__(self, line):
        print(line)

class ErrorLine(object):
    def __init__(self, line):
        print(line)

class ExceptionLine(object):
    def __init__(self, e):
        #raise(e)
        print(e)
