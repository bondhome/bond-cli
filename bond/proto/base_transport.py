from threading import Thread


class BaseTransport(object):
    def request_async(self, http_method_name, *args, **kwargs):
        on_success = kwargs.pop("on_success")
        on_error = kwargs.pop("on_error")

        def task():
            try:
                on_success(
                    self.bondid, getattr(self, http_method_name)(*args, **kwargs)
                )
            except Exception as e:
                on_error(self.bondid, e)

        t = Thread(target=task)
        t.start()
        return t
