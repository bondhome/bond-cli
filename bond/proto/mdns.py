from zeroconf import ServiceBrowser, Zeroconf

from bond.database import BondDatabase


class Listener:
    def __init__(self, on_success):
        self.on_success = on_success

    def remove_service(self, zeroconf, type, name):
        pass

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        bondid = info.name.split(".")[0]
        ip = ".".join([str(ord(chr(byte))) for byte in info.addresses[0]])
        port = info.port
        BondDatabase.set_bond(bondid, "ip", ip)
        BondDatabase.set_bond(bondid, "port", port)
        self.on_success({"bondid": bondid, "ip": ip, "port": port})

    def update_service(self, zeroconf, type, name):
        """Callback when a service is updated."""
        pass


class Scanner(object):
    def __init__(self, on_success):
        self.zeroconf = Zeroconf()
        self.listener = Listener(on_success=on_success)
        _browser = ServiceBrowser(self.zeroconf, "_bond._tcp.local.", self.listener)  # noqa: F841

    def __del__(self):
        del self.listener
        self.zeroconf.close()
