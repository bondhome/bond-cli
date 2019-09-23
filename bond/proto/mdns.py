from zeroconf import ServiceBrowser, Zeroconf
from pprint import pprint

class Listener:
    def __init__(self, callback):
        self.callback = callback

    def remove_service(self, zeroconf, type, name):
        pass

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        self.callback({
            "Bond ID": info.name.split('.')[0],
            "IP Address": '.'.join(
                [ str(ord(chr(byte))) for byte in info.addresses[0] ]),
            })

class Scanner(object):
    def __init__(self, callback):
        self.zeroconf = Zeroconf()
        self.listener = Listener(callback=callback)
        browser = ServiceBrowser(self.zeroconf,
            "_bond._tcp.local.", self.listener)

    def __del__(self):
        del self.listener
        self.zeroconf.close()
