# Mate (MT-1500) Channels API Reference

## Overview

The MT-1500 (Mate Pro) is a motor controller that supports 16 channels for controlling motorized window coverings and other devices via RF protocols. Channels allow independent configuration of different technologies (RF protocols) for controlling motors.

### Channel Structure

- **Channel 0**: Broadcast channel ("All") - sends commands to all paired motors
- **Channels 1-15**: Individual channels for specific motors or motor groups

Each channel can be configured with:
- Custom name and label (label shown on device LED matrix)
- Technology template (R-number identifier for RF protocol)
- Technology-specific properties (addresses, frequencies, etc.)
- Enabled/disabled state for visibility

## Endpoints

### List All Channels

```
GET /v2/channels
```

Returns a hash tree of all channels (0-15). The hash values indicate when channel metadata has changed.

**Example Response:**
```json
{
  "_": "7fc1e84b",
  "0": { "_": "a1b2c3d4" },
  "1": { "_": "84819a9f" },
  "2": { "_": "23141efa" },
  ...
  "15": { "_": "2425a8bc" }
}
```

**curl Example:**
```bash
curl -H "BOND-Token: $TOKEN" http://$BOND_IP/v2/channels
```

### Get Specific Channel

```
GET /v2/channels/{channel_id}
```

- `channel_id`: "0" for All channel, or "1" through "15" for individual channels

**Example Response:**
```json
{
  "name": "North Screen",
  "label": "N Screen",
  "template": "RMS12",
  "type": "MS",
  "enabled": true,
  "actions": ["Raise", "Lower", "Stop", "SetPosition"],
  "properties": {
    "mfg": 0,
    "pairing_assets_key": ""
  }
}
```

**curl Example:**
```bash
curl -H "BOND-Token: $TOKEN" http://$BOND_IP/v2/channels/1
```

### Configure Channel

```
PATCH /v2/channels/{channel_id}
```

Modifies channel metadata including name, label, technology assignment, and visibility.

**Configurable Fields:**
- `name`: User-facing name (max 64 bytes UTF-8)
- `label`: LED matrix display label (max 20 chars, A-Z, a-z, 0-9, space, "-")
- `template`: Technology template (R-number identifier)
- `enabled`: Visibility toggle (true/false)
- `properties`: Technology-specific parameters

**Note:** Channel 0 (All) only supports `name`, `label`, and `enabled` fields.

**curl Examples:**
```bash
# Set channel name and label
curl -X PATCH -H "BOND-Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Living Room Shade", "label": "LR Shade"}' \
  http://$BOND_IP/v2/channels/1

# Assign a technology template
curl -X PATCH -H "BOND-Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"template": "RMS12"}' \
  http://$BOND_IP/v2/channels/2

# Disable a channel
curl -X PATCH -H "BOND-Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"enabled": false}' \
  http://$BOND_IP/v2/channels/3
```

### Execute Channel Action

```
PUT /v2/channels/{channel_id}/actions/{action_name}
```

Executes an action on a channel by transmitting via the configured RF technology.

**Note:** This endpoint is intended for development and testing purposes. Mate is not designed to act as a bridge.

**Parameters:**
- `channel_id`: "0" through "15"
- `action_name`: Action from the channel's `actions` list

**Request Body (optional):**
```json
{
  "argument": 50
}
```

**curl Examples:**
```bash
# Raise shade
curl -X PUT -H "BOND-Token: $TOKEN" \
  http://$BOND_IP/v2/channels/1/actions/Raise

# Lower shade
curl -X PUT -H "BOND-Token: $TOKEN" \
  http://$BOND_IP/v2/channels/1/actions/Lower

# Set position to 50%
curl -X PUT -H "BOND-Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"argument": 50}' \
  http://$BOND_IP/v2/channels/1/actions/SetPosition

# Stop/Hold shade
curl -X PUT -H "BOND-Token: $TOKEN" \
  http://$BOND_IP/v2/channels/1/actions/Hold
```

## Channel Types

Channel type is automatically inferred from the configured technology template:

| Type | Description |
|------|-------------|
| `MS` | Motorized Window Coverings (Shades, Screens, Drapes, Awnings) |
| `LT` | Light |
| `CF` | Ceiling Fan |
| `GX` | Generic device |
| `FP` | Fireplace |
| `BD` | Bidet |

Channels configured for Relay mode have type `MS`.

## Common Actions

### Motorized Shades (MS)

| Action | Description |
|--------|-------------|
| `Raise` | Open the shade (move up) |
| `Lower` | Close the shade (move down) |
| `Stop` | Stop shade movement |
| `Hold` | Stop shade movement (alias for Stop) |
| `SetPosition` | Set shade to specific position (0-100, requires `argument`) |
| `Preset` | Move to preset/favorite position |

### Lights (LT)

| Action | Description |
|--------|-------------|
| `TurnLightOn` | Turn light on |
| `TurnLightOff` | Turn light off |
| `SetBrightness` | Set brightness level (requires `argument`) |

## Technology Templates

Technology templates use R-number identifiers (same format as the devices API). Example: `RMS12`

Common shade templates configure the RF protocol used for motor control. The template determines:
- RF protocol and frequency
- Available pairing procedures
- Required properties (addresses, etc.)
- Compatible motors and devices
- Available actions

## Channel Visibility

When a channel is disabled (`enabled: false`):
- Skipped during physical button cycling (Channel +/- buttons)
- Appears grayed out in the app
- Configuration is preserved (name, technology, schedules)
- Schedules for disabled channels will not execute
- For bitmap protocols (ARC, Gaposa, etc.), disabled channels are masked from channel 0 bitmap

## Requirements

- Firmware version: v4.24+
- Hardware: Mate Pro (MT-1500), also supported on Sidekick Blue (SKS-500-B)
