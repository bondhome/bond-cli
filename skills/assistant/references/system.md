# System Operations Reference

Bond Local API system-level endpoints for device management, diagnostics, and configuration.

## Version Information

**Endpoint:** `GET /v2/sys/version`

No token required. Returns hardware and firmware details.

```bash
curl http://<bond-ip>/v2/sys/version
```

**Response fields:**
- `bondid`: Serial number (unique identifier)
- `target`: Firmware target (e.g., `zermatt`, `breck`)
- `fw_ver`: Firmware version (e.g., `v2.9`, `v2.9.1-beta`)
- `fw_date`: Build date (human-readable)
- `model`: Device model number (e.g., `BD-1000`)
- `make`: Manufacturer (e.g., `Olibra LLC`)
- `api`: API version number
- `upgrade_http`: If true, use HTTP instead of HTTPS for upgrades

## Time and Location

**Endpoint:** `GET /v2/sys/time` | `PATCH /v2/sys/time`

Manage system time, timezone, and location for schedules.

```bash
# Get current time settings
curl -H "BOND-Token: <token>" http://<bond-ip>/v2/sys/time

# Set timezone and grid location
curl -X PATCH -H "BOND-Token: <token>" \
  -d '{"tz": "America/New_York", "grid": "FN30aw"}' \
  http://<bond-ip>/v2/sys/time
```

**Fields:**
- `unix_time`: Seconds since UNIX epoch
- `time_set`: Boolean - true if time has been set via NTP
- `tz`: Timezone string (e.g., `America/Sao_Paulo`). See [supported timezones](https://bond-updates.s3.amazonaws.com/tz_meta.json)
- `grid`: 6-character Maidenhead Grid Locator for sunrise/sunset calculations (e.g., `FN30aw`)

**Note:** Setting `tz` to `null` disables midnight-based schedules. Setting `grid` to `null` disables solar-based schedules.

## Reboot

**Endpoint:** `PUT /v2/sys/reboot`

Reboot the Bond. No settings are modified.

```bash
curl -X PUT -H "BOND-Token: <token>" http://<bond-ip>/v2/sys/reboot
```

## Reset

**Endpoint:** `PUT /v2/sys/reset`

Perform a setup or factory reset.

```bash
# Setup reset (allows re-pairing without data loss)
curl -X PUT -H "BOND-Token: <token>" \
  -d '{"type": "setup"}' \
  http://<bond-ip>/v2/sys/reset

# Factory reset (ERASES ALL DATA)
curl -X PUT -H "BOND-Token: <token>" \
  -d '{"type": "factory"}' \
  http://<bond-ip>/v2/sys/reset
```

**Reset types:**
- `setup`: Re-enables Config AP and allows new Wi-Fi/account setup. Devices preserved. No reboot.
- `factory`: **ERASES ALL devices and settings.** Bond reboots. Firmware version preserved.

**WARNING:** Factory reset is irreversible. All devices, schedules, and configurations will be permanently deleted. Ensure you have a backup before proceeding.

## Firmware Upgrade

### Start Upgrade

**Endpoint:** `PUT /v2/sys/upgrade`

```bash
curl -X PUT -H "BOND-Token: <token>" \
  -d '{
    "host": "s3.amazonaws.com",
    "port": "443",
    "http_port": "80",
    "path": "/bond-updates/zermatt-v2.10.bin",
    "info": "<sha256>:<target>:<version>",
    "sig": "<base64-signature>",
    "reboot": 1
  }' \
  http://<bond-ip>/v2/sys/upgrade
```

**Required fields:**
- `host`: FQDN or IP of download server
- `port`: HTTPS port (used unless `upgrade_http` is true in version)
- `path`: Path to firmware binary (must start with `/`)
- `info`: Format: `<sha256-hash>:<target>:<version>`
- `sig`: Base64-encoded signature of `info` string

**Optional fields:**
- `http_port`: HTTP port (used if `upgrade_http` is true)
- `reboot`: Set to `1` for automatic reboot after upgrade; `0` requires manual reboot via `/v2/sys/reboot`

### Check Progress

**Endpoint:** `GET /v2/sys/upgrade`

```bash
curl -H "BOND-Token: <token>" http://<bond-ip>/v2/sys/upgrade
```

**Response:**
- `204 No Content`: No upgrade in progress
- `200 OK`: Returns progress object

**Progress values:**
- `1-999`: Progress in tenths of a percent (e.g., 500 = 50%)
- `1000`: Upgrade complete, waiting for reboot
- `-1`: Error (see `error_msg`)

### Cancel Upgrade

**Endpoint:** `DELETE /v2/sys/upgrade`

```bash
curl -X DELETE -H "BOND-Token: <token>" http://<bond-ip>/v2/sys/upgrade
```

Canceling is always safe. **WARNING:** Do not power cycle during an upgrade.

## Backup and Restore

**Endpoint:** `PUT /v2/sys/backup` | `GET /v2/sys/backup` | `DELETE /v2/sys/backup`

Backup/restore devices to/from a local HTTP server.

```bash
# Start backup
curl -X PUT -H "BOND-Token: <token>" \
  -d '{
    "host": "192.168.1.107",
    "http_port": "8080",
    "path": "/snapshots",
    "timestamp": "1618599782"
  }' \
  http://<bond-ip>/v2/sys/backup

# Start restore
curl -X PUT -H "BOND-Token: <token>" \
  -d '{
    "host": "192.168.1.107",
    "http_port": "8080",
    "path": "/snapshots",
    "filename": "/ZZDE12345_v2.18.4_1618599782_0f8d01fa.bsnap"
  }' \
  http://<bond-ip>/v2/sys/backup

# Check status
curl -H "BOND-Token: <token>" http://<bond-ip>/v2/sys/backup

# Clear status after completion
curl -X DELETE -H "BOND-Token: <token>" http://<bond-ip>/v2/sys/backup
```

**Status fields:**
- `backup`/`restore`: `0` = idle, `1` = running, `2` = success, `-1` = failure
- `progress`: 0-1000 (1000 = complete)
- `error_msg`: Present on failure

**Note:** Backup includes devices, commands, properties, state, and schedules. Network settings and bridge name/location are NOT included. Restore is additive (updates existing, creates new).

## Wi-Fi Configuration

### Scan for Networks

**Endpoint:** `GET /v2/sys/wifi/scan`

```bash
curl -H "BOND-Token: <token>" http://<bond-ip>/v2/sys/wifi/scan
```

Returns `204` if no scan completed yet. Initiates a new scan on each request.

**Response format:**
- `format`: Column names for results array (ssid, bssid, auth, ch, signal)
- `results`: 2D array of network data
- `hidden_requires_bssid`: If true, hidden networks need BSSID to connect

**Auth types:** 0=Open, 1=WEP, 2=WPA, 3=WPA2, 4=WPA/WPA2, 5=Enterprise (unsupported)

**Note:** `ssid` values are base64-encoded.

### Station Configuration

**Endpoint:** `GET /v2/sys/wifi/sta` | `PATCH /v2/sys/wifi/sta` | `DELETE /v2/sys/wifi/sta`

```bash
# Get current Wi-Fi status
curl -H "BOND-Token: <token>" http://<bond-ip>/v2/sys/wifi/sta

# Connect to network (ssid and password are base64-encoded)
curl -X PATCH -H "BOND-Token: <token>" \
  -d '{"ssid": "bXluZXR3b3Jr", "password": "bXlwYXNzd29yZA=="}' \
  http://<bond-ip>/v2/sys/wifi/sta

# Disconnect (forgets network)
curl -X DELETE -H "BOND-Token: <token>" http://<bond-ip>/v2/sys/wifi/sta
```

**Status codes:**
- `-4`: Wi-Fi not configured
- `-3`: Disabled (Ethernet selected)
- `-2`: Authentication failure
- `-1`: Network not found
- `0`: Connecting
- `1`: Connected, no IP
- `2`: Connected with IP
- `3`: Connected to cloud (MQTT)

**Optional fields for static IP:**
- `static_ip_set`: true + `ip`, `gw`, `netmask`
- `dns_set`: true + `dns`, `dns_alt`

## Bridge Information

**Endpoint:** `GET /v2/bridge` | `PATCH /v2/bridge`

```bash
# Get bridge info
curl -H "BOND-Token: <token>" http://<bond-ip>/v2/bridge

# Update bridge settings
curl -X PATCH -H "BOND-Token: <token>" \
  -d '{"name": "Living Room Bridge", "location": "Living Room", "bluelight": 50}' \
  http://<bond-ip>/v2/bridge
```

**Fields:**
- `name`: User-assigned bridge name
- `location`: User-assigned location
- `bluelight`: LED brightness when idle (0-255, where 0=off, 255=max)
- `frequencies`: (read-only) Supported RF/IR frequency ranges in kHz

## LED Indication

**Endpoint:** `GET /v2/sys/indicate` | `PATCH /v2/sys/indicate`

Trigger visual indication on supported devices (Mate Pro MT-1500, v4.26+).

```bash
# Trigger identify animation for 10 seconds
curl -X PATCH -H "BOND-Token: <token>" \
  -d '{"identify": 10}' \
  http://<bond-ip>/v2/sys/indicate

# Trigger commit animation for 3 seconds
curl -X PATCH -H "BOND-Token: <token>" \
  -d '{"commit": 3}' \
  http://<bond-ip>/v2/sys/indicate

# Cancel animation
curl -X PATCH -H "BOND-Token: <token>" \
  -d '{"identify": 0}' \
  http://<bond-ip>/v2/sys/indicate
```

**Animation types:**
- `identify`: Radar/sonar expanding circles (1-30 seconds)
- `commit`: Checkmark confirmation (1-30 seconds)
- Set to `0` to cancel

Animations are mutually exclusive and can be dismissed by pressing any device button.

---

## Safety Warnings

**Reset operations:**
- `factory` reset is **IRREVERSIBLE** and deletes all devices and configurations
- Always create a backup before factory reset
- `setup` reset is safe and preserves device data

**Upgrade operations:**
- **NEVER power cycle during firmware upgrade** - may brick the device
- Canceling an upgrade via `DELETE` is always safe
- Allow up to 7 minutes for slow networks before declaring timeout
- After upgrade, verify success by checking `/v2/sys/version`

**Wi-Fi operations:**
- `DELETE /v2/sys/wifi/sta` disconnects and forgets the network
- Bond will not reconnect until reconfigured
- Keep the Bond accessible (Config AP or Ethernet) when changing Wi-Fi settings
