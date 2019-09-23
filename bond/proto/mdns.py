from zeroconf import ServiceBrowser, Zeroconf
import bond.database

def get_ip(bondid):
    mdns_cache = bond.database.get('mdns_cache')
    if bondid not in mdns_cache:
        raise Exception("Bond ID not in cache. Use 'bond discover' first.")
    return mdns_cache[bondid]

def update_cache(bondid, ip):
    mdns_cache = bond.database.get('mdns_cache')
    if not mdns_cache:
        mdns_cache = dict()
    mdns_cache[bondid] = ip
    bond.database.set('mdns_cache', mdns_cache)

class Listener:
    def __init__(self, on_success):
        self.on_success = on_success

    def remove_service(self, zeroconf, type, name):
        pass

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        bondid = info.name.split('.')[0]
        ip = '.'.join([ str(ord(chr(byte))) for byte in info.addresses[0] ])
        update_cache(bondid, ip)
        self.on_success({
            'bondid': bondid,
            'ip': ip,
            })

class Scanner(object):
    def __init__(self, on_success):
        self.zeroconf = Zeroconf()
        self.listener = Listener(on_success=on_success)
        browser = ServiceBrowser(self.zeroconf,
            "_bond._tcp.local.", self.listener)

    def __del__(self):
        del self.listener
        self.zeroconf.close()
