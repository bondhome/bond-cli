---
name: assistant
description: Control Bond Home smart devices - ceiling fans, shades, lights, fireplaces. Use when user wants to control smart home devices, check device status, turn on/off fans or lights, open/close shades, or adjust device settings.
---

# Bond Home Assistant

Control Bond Home smart devices via the Local API.

## Quick Reference

| Operation | Endpoint | Method |
|-----------|----------|--------|
| List devices | `/v2/devices` | GET |
| Device info | `/v2/devices/{id}` | GET |
| Device state | `/v2/devices/{id}/state` | GET |
| Execute action | `/v2/devices/{id}/actions/{action}` | PUT |
| Device properties | `/v2/devices/{id}/properties` | GET |

## Database Location

Bond CLI stores discovered Bonds at `~/.bond/db.json`:

```json
{
  "bonds": {
    "BONDID12345": {
      "ip": "192.168.1.100",
      "port": 80,
      "token": "abc123def456"
    }
  },
  "selected": "BONDID12345"
}
```

Read this file to get Bond IPs and tokens. If empty or missing, guide user to run `bond discover`.

## API Pattern

All requests (except `/v2/sys/version` and `/v2/token`) require the token header:

```bash
curl -H "BOND-Token: {token}" http://{ip}:{port}/v2/...
```

## Common Operations

### List All Devices

```bash
curl -H "BOND-Token: {token}" http://{ip}:{port}/v2/devices
```

Response contains device IDs as keys. Fetch each device for details.

### Get Device Details

```bash
curl -H "BOND-Token: {token}" http://{ip}:{port}/v2/devices/{device_id}
```

Returns:
```json
{
  "name": "Living Room Fan",
  "type": "CF",
  "location": "Living Room",
  "actions": ["TurnOn", "TurnOff", "SetSpeed", ...],
  "_": "hash"
}
```

### Check Device State

```bash
curl -H "BOND-Token: {token}" http://{ip}:{port}/v2/devices/{device_id}/state
```

Returns current state (power, speed, light, position, etc.).

### Turn On / Turn Off

```bash
# Turn on
curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}:{port}/v2/devices/{device_id}/actions/TurnOn

# Turn off
curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}:{port}/v2/devices/{device_id}/actions/TurnOff
```

### Set Fan Speed

```bash
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": 3}' \
  http://{ip}:{port}/v2/devices/{device_id}/actions/SetSpeed
```

Speed is 1 to max_speed (check device properties).

### Open / Close Shades

```bash
# Open
curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}:{port}/v2/devices/{device_id}/actions/Open

# Close
curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}:{port}/v2/devices/{device_id}/actions/Close

# Set position (0=open, 100=closed)
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": 50}' \
  http://{ip}:{port}/v2/devices/{device_id}/actions/SetPosition
```

### Control Lights

```bash
# Turn light on/off (for fans with lights)
curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}:{port}/v2/devices/{device_id}/actions/TurnLightOn

curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}:{port}/v2/devices/{device_id}/actions/TurnLightOff

# Set brightness (1-100)
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": 75}' \
  http://{ip}:{port}/v2/devices/{device_id}/actions/SetBrightness
```

## Device Types

| Code | Type | Common Actions |
|------|------|----------------|
| CF | Ceiling Fan | TurnOn, TurnOff, SetSpeed, TurnLightOn, TurnLightOff |
| MS | Motorized Shades | Open, Close, SetPosition, Hold |
| LT | Light | TurnOn, TurnOff, SetBrightness |
| FP | Fireplace | TurnOn, TurnOff, SetFlame |
| HT | Heater | TurnOn, TurnOff, SetHeat |

## Device Matching

When user refers to a device by name or location:

1. **List all devices** across all known Bonds
2. **Match by name** (case-insensitive, partial match OK)
3. **Match by location** if name doesn't match
4. **Match by type** if user says "fan", "light", "shade"
5. **Ask user** if multiple devices match or none match

Example: "turn on the bedroom fan"
- Search for devices where `name` or `location` contains "bedroom"
- Filter by `type: "CF"` for fans
- If one match, execute. If multiple, ask which one.

## Safety Model

**Liberal for actions:** Execute device controls (TurnOn, SetSpeed, Open, etc.) without confirmation.

**Careful for destructive operations:**
- Factory reset
- Firmware upgrade
- Deleting devices

Always confirm these with the user first.

## Reference Documents

For advanced operations, see the reference documents in `references/`:

| Document | Domain |
|----------|--------|
| [discovery-auth.md](references/discovery-auth.md) | mDNS discovery, token retrieval, PIN unlock |
| [actions-fan.md](references/actions-fan.md) | Ceiling fan: breeze, direction, up/down lights |
| [actions-shades.md](references/actions-shades.md) | Shades: position, tilt, TDBU, sheer/blackout |
| [actions-light.md](references/actions-light.md) | Lights: color, colorTemp, RGB, HSV |
| [actions-fireplace.md](references/actions-fireplace.md) | Fireplace/heater: flame, heat, timer |
| [device-types.md](references/device-types.md) | Full type/capability matrix |
| [groups-scenes.md](references/groups-scenes.md) | Multi-device control |
| [schedules.md](references/schedules.md) | Time-based automation |
| [mate-channels.md](references/mate-channels.md) | MT-1500 motor controller |
| [system.md](references/system.md) | Reboot, upgrade, wifi, backup |
| [signals.md](references/signals.md) | RF/IR transmission (Bridge only) |
| [troubleshooting.md](references/troubleshooting.md) | Common errors |

## Workflow

1. **Read database** at `~/.bond/db.json` to get Bond IPs and tokens
2. **List devices** on each Bond
3. **Match device** to user's request
4. **Execute action** via PUT to actions endpoint
5. **Verify state** if needed via GET to state endpoint
6. **Report result** to user
