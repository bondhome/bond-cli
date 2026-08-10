# Discovery & Authentication

## mDNS Discovery

Bond devices advertise via mDNS service type `_bond._tcp.local.`.

### Using Python (zeroconf)

```python
from zeroconf import ServiceBrowser, Zeroconf
import socket

class BondListener:
    def add_service(self, zc, type_, name):
        info = zc.get_service_info(type_, name)
        if info:
            ip = socket.inet_ntoa(info.addresses[0])
            bond_id = name.split('.')[0]
            print(f"Found Bond: {bond_id} at {ip}:{info.port}")

zc = Zeroconf()
browser = ServiceBrowser(zc, "_bond._tcp.local.", BondListener())
# Keep running to discover...
```

### Using Command Line

**macOS:**
```bash
dns-sd -B _bond._tcp .
# Then resolve specific Bond:
dns-sd -L BONDID12345 _bond._tcp .
```

**Linux:**
```bash
avahi-browse -a | grep bond
```

### Using bond-cli

```bash
bond discover
```

This populates `~/.bond/db.json` with found Bonds.

## Database Structure

Bond CLI stores data in `~/.bond/db.json`:

```json
{
  "bonds": {
    "ZZBL12345": {
      "ip": "192.168.1.100",
      "port": 80,
      "token": "f074b61f628018fd",
      "name": "Living Room Bridge"
    },
    "KSMJWCE12345": {
      "ip": "192.168.1.101",
      "port": 80,
      "token": "a1b2c3d4e5f67890",
      "name": "Master Bedroom Fan"
    }
  },
  "selected": "ZZBL12345"
}
```

Key fields:
- `ip`: IP address on local network
- `port`: HTTP port (default 80)
- `token`: Authentication token (16 hex chars)
- `selected`: Currently active Bond for CLI commands

## Token Retrieval

Tokens are required for all API endpoints except:
- `GET /v2/sys/version`
- `GET /v2/token`

### Method 1: Power Cycle Window (10 minutes)

After power cycling a Bond, the token is accessible for 10 minutes:

```bash
curl http://{ip}/v2/token
```

Response:
```json
{
  "locked": 0,
  "token": "f074b61f628018fd",
  "pin_attempts_left": 10
}
```

### Method 2: PIN Unlock

Use the 4-digit PIN from the product label:

```bash
curl -X PATCH http://{ip}/v2/token \
  -H "Content-Type: application/json" \
  -d '{"pin": "1234"}'
```

Response:
```json
{
  "locked": 0,
  "token": "f074b61f628018fd"
}
```

After retrieving the token, re-lock:

```bash
curl -X PATCH http://{ip}/v2/token \
  -H "Content-Type: application/json" \
  -d '{"locked": 1}'
```

### Method 3: Using bond-cli

```bash
# Set token manually (if you know it)
bond token --set f074b61f628018fd

# Unlock with PIN
bond token --unlock 1234
```

## Token Header Format

All authenticated requests require the `BOND-Token` header:

```bash
curl -H "BOND-Token: f074b61f628018fd" http://{ip}/v2/devices
```

Alternative: Embed token in request body (since v2.6.23):

```bash
curl http://{ip}/v2/devices -X GET \
  -d '{"_token": "f074b61f628018fd"}'
```

## Common Auth Errors

### 401 Unauthorized

**Missing token:**
```bash
curl http://{ip}/v2/devices
# Returns 401
```
Solution: Add `BOND-Token` header.

**Invalid token:**
```bash
curl -H "BOND-Token: wrongtoken" http://{ip}/v2/devices
# Returns 401
```
Solution: Retrieve correct token via power cycle or PIN unlock.

### Token Locked

If `GET /v2/token` returns `"locked": 1`:

1. Power cycle the Bond and retry within 10 minutes, OR
2. Use PIN unlock with `PATCH /v2/token`

### PIN Attempts Exhausted

If `pin_attempts_left` reaches 0, wait 30 minutes or power cycle the Bond.

## Bond ID Prefixes

Bond IDs indicate device type:

| Prefix | Device Type |
|--------|-------------|
| ZZ | Bond Bridge (original) |
| BD | Bond Bridge Pro |
| K | Smart by Bond (SBB) device |

## Version Check (No Auth Required)

Always works without token:

```bash
curl http://{ip}/v2/sys/version
```

Response:
```json
{
  "target": "snowbird",
  "fw_ver": "v3.0.0",
  "make": "Olibra",
  "model": "BD1000",
  "bondid": "ZZBL12345"
}
```

Use this to verify connectivity before attempting authenticated requests.
