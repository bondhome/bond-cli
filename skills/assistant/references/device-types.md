# Bond Device Types Reference

## Device Type Codes

| Code | Name | Description |
|------|------|-------------|
| `CF` | Ceiling Fan | Multi-speed ceiling fans with optional light and direction control |
| `MS` | Motorized Shades | Motorized window coverings including shades, screens, drapes, and awnings |
| `LT` | Light | Standalone lighting devices |
| `FP` | Fireplace | Gas or electric fireplaces with flame control |
| `BD` | Bidet | Smart bidet devices |
| `GX` | Generic | Generic device type for devices that don't fit other categories |
| `HT` | Heater | Heating devices with heat level control |

The `type` field does not impact device functionality. It is used by API clients to improve user experience (e.g., selecting appropriate icons) and by integrations to determine device categories for platforms like Google Assistant or Alexa.

## Subtypes

### Motorized Shades (MS) Subtypes

| Subtype | Description |
|---------|-------------|
| `ROLLER` | Roller blackout shade which blocks light and provides privacy |
| `SHEER` | Shade which permits light to pass and does not provide privacy |
| `AWNING` | Outdoor patio covering |

**Note:** The `subtype` field is for analytics and aesthetics only. New subtypes may be introduced without notice. API clients should always fall back to a reasonable default based on the device `type`.

## Capabilities Matrix

| Feature | CF | MS | LT | FP | BD | GX | HT |
|---------|----|----|----|----|----|----|-----|
| Power | Yes | - | Yes | Yes | Yes | Yes | Yes |
| Speed | Yes | - | - | - | - | - | - |
| Breeze | Yes | - | - | - | - | - | - |
| Direction | Yes | - | - | - | - | - | - |
| Light | Yes | - | Yes | Yes | - | - | - |
| Brightness | Yes | - | Yes | Yes | - | - | - |
| UpDownLight | Yes | - | - | - | - | - | - |
| ColorTemp | - | - | Yes | - | - | - | - |
| Color (RGB) | - | - | Yes | - | - | - | - |
| Open | - | Yes | - | - | - | - | - |
| Position | - | Yes | - | - | - | - | - |
| TiltPosition | - | Yes | - | - | - | - | - |
| TDBU | - | Yes | - | - | - | - | - |
| Flame | - | - | - | Yes | - | - | - |
| FpFan | - | - | - | Yes | - | - | - |
| Heat | - | - | - | - | - | - | Yes |
| Timer | Yes | - | - | - | - | - | Yes |
| Pair | - | Yes | - | - | - | - | - |
| Hold | - | Yes | - | - | - | - | - |
| Preset | - | Yes | - | - | - | - | - |

## Common Properties by Type

### Ceiling Fan (CF)
- `max_speed`: (integer, read-only) Highest speed available
- `feature_light`: (boolean) Enable/disable light feature
- `feature_brightness`: (boolean) Enable/disable brightness control
- `feature_up_down_light`: (boolean) Enable/disable separate up/down light control

### Motorized Shades (MS)
- `feature_position`: (boolean) Enable/disable position control
- `course_time`: (integer) Time in milliseconds for shade to fully open/close (for dead reckoning position emulation)
- `min_tilt`: (integer) Minimum tilt position in degrees (default 0)
- `max_tilt`: (integer) Maximum tilt position in degrees (default 90)

### Heater (HT)
- `feature_heat`: (boolean) Enable/disable heat level control
- `default_auto_timer_s`: (integer) Auto-timer duration in seconds for fire code compliance (commonly 2 hours)

### Light (LT)
- `feature_brightness`: (boolean) Enable/disable brightness control
- `max_color_temp`: (integer) Maximum color temperature in Kelvin
- `min_color_temp`: (integer) Minimum color temperature in Kelvin

### Fireplace (FP)
- `feature_light`: (boolean) Enable/disable light feature (many fireplaces have separate lights)

### Bridge Properties (RF Devices)
- `addr`: (string, read-only) Device address
- `freq`: (integer, read-only) RF frequency in Hz
- `bps`: (integer, read-only) Bits per second
- `zero_gap`: (integer, read-only) Length of zeros between repetitions
- `trust_state`: (boolean) Whether Bond should trust its toggleable state belief

## Template Codes

Templates define the protocol and default controls for a device. When POSTing a new device with a valid `template` string, the device self-populates its panel with default controls, initializes state, and loads the appropriate behavior script.

Common template parameters:
- `addr`: Device address
- `freq`: RF frequency
- `bps`: Bits per second
- `zero_gap`: Gap between transmissions

Example template: `"A1"` (specific templates vary by device manufacturer and protocol)

## API Endpoints

### Get Device Information

```bash
# List all devices
curl -H "BOND-Token: <token>" http://<bond-ip>/v2/devices

# Get specific device details
curl -H "BOND-Token: <token>" http://<bond-ip>/v2/devices/<device-id>
```

**Response example:**
```json
{
  "name": "My Fan",
  "type": "CF",
  "location": "Living Room",
  "actions": ["TurnOn", "TurnOff", "SetSpeed", "IncreaseSpeed", "DecreaseSpeed"],
  "properties": {"_": "84cd8a43"},
  "state": {"_": "ad9bcde4"},
  "commands": {"_": "be8e1896"},
  "_": "599b0fc5"
}
```

### Get Device State

```bash
curl -H "BOND-Token: <token>" http://<bond-ip>/v2/devices/<device-id>/state
```

**Response example (Ceiling Fan):**
```json
{
  "power": 1,
  "speed": 3,
  "light": 1,
  "brightness": 75,
  "direction": 1,
  "breeze": [1, 50, 50],
  "timer": 0,
  "_": "ab9284ef"
}
```

**Response example (Motorized Shade):**
```json
{
  "open": 1,
  "position": 50,
  "_": "cd1234ef"
}
```

### Get Device Properties

```bash
curl -H "BOND-Token: <token>" http://<bond-ip>/v2/devices/<device-id>/properties
```

**Response example (Ceiling Fan):**
```json
{
  "max_speed": 6,
  "feature_light": true,
  "feature_brightness": true,
  "trust_state": false,
  "addr": "10101",
  "freq": 434300,
  "bps": 3000,
  "_": "84cd8a43"
}
```

### Execute Device Action

```bash
# Turn on device
curl -H "BOND-Token: <token>" -X PUT \
  http://<bond-ip>/v2/devices/<device-id>/actions/TurnOn

# Set speed with argument
curl -H "BOND-Token: <token>" -X PUT \
  -d '{"argument": 3}' \
  http://<bond-ip>/v2/devices/<device-id>/actions/SetSpeed

# Set brightness
curl -H "BOND-Token: <token>" -X PUT \
  -d '{"argument": 75}' \
  http://<bond-ip>/v2/devices/<device-id>/actions/SetBrightness
```

## State Variables by Feature

### Power Feature
- `power`: (integer) 1 = on, 0 = off

### Speed Feature
- `speed`: (integer) 1 to max_speed

### Breeze Feature
- `breeze`: (array) `[mode, mean, var]` where mode is 0/1, mean and var are 0-100

### Direction Feature
- `direction`: (integer) 1 = forward, -1 = reverse

### Light Feature
- `light`: (integer) 1 = on, 0 = off

### Brightness Feature
- `brightness`: (integer) 1-100 percent

### Open Feature
- `open`: (integer) 1 = open, 0 = closed

### Position Feature
- `position`: (integer) 0-100 where 0 = open, 100 = closed

### Flame Feature
- `flame`: (integer) 1-100

### Heat Feature
- `heat`: (integer) 1-100

### Timer Feature
- `timer`: (integer) seconds remaining, 0 = no timer

### ColorTemp Feature
- `color_temp`: (integer) color temperature in Kelvin

### Color Feature
- `rgb`: (object) `{r: 0-255, g: 0-255, b: 0-255}`
- `hsv`: (object) `{h: 0-359, s: 0-100, v: 0-100}`
