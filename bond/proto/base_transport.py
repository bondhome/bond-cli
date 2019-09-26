from threading import Thread
from collections import defaultdict


class BaseTransport(object):
    def get_async(self, *args, **kwargs):
        kwargs = defaultdict(lambda: lambda x: {}, kwargs)
        on_success = kwargs["on_success"]
        del kwargs["on_success"]
        on_error = kwargs["on_error"]
        del kwargs["on_error"]

        def task():
            try:
                on_success(self.bondid, self.get(*args, **kwargs))
            except Exception as e:
                on_error(self.bondid, e)

        t = Thread(target=task)
        t.start()
        return t

    # TODO: other methods
