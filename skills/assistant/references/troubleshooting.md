# Troubleshooting Guide

## Connection Issues

### Bond Not Responding

1. **Check IP address** - Verify the Bond's IP hasn't changed (DHCP lease renewal)
2. **Ping the Bond** - `ping {ip}` to verify network connectivity
3. **Check power** - Ensure the Bond is powered on (LEDs should be visible)
4. **Check version (no auth required)** - `curl http://{ip}/v2/sys/version`

## Authentication Errors

### 401 Unauthorized

- **Invalid or missing token** - The `BOND-Token` header is required for most endpoints
- **Token retrieval options:**
  - Power cycle the Bond and use the temporary unlock window
  - Use PIN unlock if configured
  - See [discovery-auth.md](discovery-auth.md) for detailed authentication procedures

## Device Not Found

- **Re-run discovery** - `bond discover` to find Bonds on the network
- **Check device assignment** - Verify the device is on the correct Bond
- **Device may have been deleted** - Check the Bond's device list

## Action Errors

### 400 Bad Request

- **Device doesn't support action** - Check the device type and its capabilities
- **Invalid argument** - Verify action argument requirements match the device type
- **Check device properties** - Some actions require specific device configurations

## State Not Updating

- **RF devices are "fire and forget"** - There is no confirmation from the physical device
- **Use `trust_state` property** - Enable state tracking for devices that support it
- **State is best-effort** - The Bond tracks what it believes the state to be, but cannot verify

## Network Issues

- **Bond on different subnet** - Ensure your client is on the same network segment
- **Firewall blocking mDNS** - Port 5353 UDP must be open for discovery
- **Firewall blocking HTTP** - Port 80 TCP must be open for API access
- **Router isolation** - Some routers isolate wireless clients; check AP settings

## Debug Endpoints (Bridge-Only)

These endpoints are available only on Bond Bridge hardware for advanced debugging.

### LiveLog - Real-time Log Output

```
GET /v2/debug/livelog
PUT /v2/debug/livelog
DELETE /v2/debug/livelog
```

Configure the Bond to send UDP log packets to a specified IP and port. Every log message is sent in a separate UDP packet. Note: High log verbosity may cause performance problems.

Settings do not persist past reboot.

### WiFi Diagnostics

```
GET /v2/debug/wifi
PATCH /v2/debug/wifi
```

Get or set Wi-Fi power settings. The `shutdown` field controls radio power:
- `0`: Normal operation
- `1`: Low-power shutdown mode

Settings do not persist past reboot.

### RF Manager Status

```
GET /v2/debug/rfman
PATCH /v2/debug/rfman
DELETE /v2/debug/rfman
```

Debug RF signal generation:
- `silence_tx`: Stop Bond from transmitting (LEDs still flash, state changes)
- `log_signals`: Send all signals to BPUP listeners on topic `debug/rfman/signal`

All values are false by default. Settings do not persist past reboot.

### LED Control

```
GET /v2/debug/leds
PATCH /v2/debug/leds
```

Manually control LEDs for testing:
- `manual`: Set to `1` to disable automatic LED control
- `value`: Concatenated 24-bit RGB hex values for each LED

### Database Statistics

```
GET /v2/debug/beau/{partition}
```

Get statistics about Bond databases. Partitions:
- `db`: Main read-write database (devices and settings)
- `id`: Read-only partition (Bond ID and certificates)
- `state`: Device state storage (Bridges only)

## HTTP Status Codes Reference

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 200  | OK | Request successful |
| 201  | Created | Resource created successfully |
| 204  | No Content | Request successful, no response body |
| 400  | Bad Request | Invalid JSON, unsupported action, invalid arguments |
| 401  | Unauthorized | Missing or invalid `BOND-Token` header |
| 404  | Not Found | Device, Bond, or endpoint doesn't exist |
| 409  | Conflict | Resource conflict (e.g., duplicate ID) |
| 423  | Locked | Resource is locked |
| 500  | Internal Server Error | Unexpected server-side error |
