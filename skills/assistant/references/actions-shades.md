# Motorized Shades Actions Reference

## Device Type

- **Type**: `MS` (Motorized Shades)
- **Subtypes**: `ROLLER`, `SHEER`, `AWNING`

## Features Overview

Motorized shades can support various combinations of the following features:
- **Open**: Basic open/close control
- **Position**: Percentage-based positioning (0=open, 100=closed)
- **Hold**: Stop motion mid-travel
- **Preset**: Go to saved favorite position
- **TiltPosition**: Tilt control for venetian blinds
- **TDBU**: Top-Down Bottom-Up dual rail control
- **SheerBlackoutDuo**: Dual-layer sheer and blackout fabric control

---

## Open/Close Feature

Basic open and close control for motorized shades.

### State Variables

| Variable | Type | Description |
|----------|------|-------------|
| `open` | integer | 1 = open, 0 = closed |

### Actions

#### Open
Open the shade completely.

```bash
curl -X PUT -H "BOND-Token: {token}" http://{ip}/v2/devices/{id}/actions/Open
```

#### Close
Close the shade completely.

```bash
curl -X PUT -H "BOND-Token: {token}" http://{ip}/v2/devices/{id}/actions/Close
```

#### ToggleOpen
Toggle between open and closed states.

```bash
curl -X PUT -H "BOND-Token: {token}" http://{ip}/v2/devices/{id}/actions/ToggleOpen
```

---

## Position Feature

Percentage-based position control. Requires the Open feature.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `feature_position` | boolean | Enable/disable position feature (PATCH-able) |
| `course_time` | integer | Time in milliseconds for full open/close travel. Required for dead-reckoning position on shades without native position support. Defaults to -1 (unconfigured). |

### State Variables

| Variable | Type | Description |
|----------|------|-------------|
| `position` | integer | 0 = fully open, 100 = fully closed |

### Actions

#### SetPosition
Set shade to a specific position percentage.

```bash
curl -X PUT -H "BOND-Token: {token}" \
  -d '{"argument": 50}' \
  http://{ip}/v2/devices/{id}/actions/SetPosition
```

#### IncreasePosition
Close the shade by a specified percentage of the full range.

```bash
curl -X PUT -H "BOND-Token: {token}" \
  -d '{"argument": 10}' \
  http://{ip}/v2/devices/{id}/actions/IncreasePosition
```

#### DecreasePosition
Open the shade by a specified percentage of the full range.

```bash
curl -X PUT -H "BOND-Token: {token}" \
  -d '{"argument": 10}' \
  http://{ip}/v2/devices/{id}/actions/DecreasePosition
```

---

## Hold Feature

Stop shade motion mid-travel.

### Actions

#### Hold
Stop the motion of the shade. The shade will be in an unknown position state and will show as open.

**Note**: For Somfy RTS shades, the same command is used for both Hold and Preset (My), so calling Hold while the shade is not moving will send it to the preset position instead.

```bash
curl -X PUT -H "BOND-Token: {token}" http://{ip}/v2/devices/{id}/actions/Hold
```

---

## Preset Feature

Move shade to a saved favorite position.

### Actions

#### Preset
Move the shade to the preset position (also known as "My" or "Favorite" position).

**Note**: Bond Bridge does not know the percentage of the preset position, so position will report as -1 (unknown) after this action unless the shade has two-way communication.

```bash
curl -X PUT -H "BOND-Token: {token}" http://{ip}/v2/devices/{id}/actions/Preset
```

---

## TiltPosition Feature

Tilt control for venetian blinds and similar slat-based shades.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `min_tilt` | integer | Minimum tilt position in degrees (default 0). Traditional wooden blinds tilt approximately 180 degrees (-90 to 90), with 0 being horizontal. |
| `max_tilt` | integer | Maximum tilt position in degrees (default 90). |

### State Variables

| Variable | Type | Description |
|----------|------|-------------|
| `tilt_position` | integer | Angle of slats in degrees |

### Actions

#### SetTiltPosition
Set slats to a specific tilt position in degrees.

```bash
curl -X PUT -H "BOND-Token: {token}" \
  -d '{"argument": 45}' \
  http://{ip}/v2/devices/{id}/actions/SetTiltPosition
```

#### ToggleTilt
Toggle slats between open and closed positions.

```bash
curl -X PUT -H "BOND-Token: {token}" http://{ip}/v2/devices/{id}/actions/ToggleTilt
```

---

## TDBU Feature (Top-Down Bottom-Up)

Dual rail control for top-down bottom-up shades. Requires the Position feature.

### State Variables

| Variable | Type | Description |
|----------|------|-------------|
| `upper_rail_position` | integer | 0 = open (at top), 100 = closed (lowered) |
| `lower_rail_position` | integer | 0 = open (raised), 100 = closed (at bottom) |

### Actions

#### SetUpperRailPosition
Set the position of the upper rail (top-down).

```bash
curl -X PUT -H "BOND-Token: {token}" \
  -d '{"argument": 30}' \
  http://{ip}/v2/devices/{id}/actions/SetUpperRailPosition
```

#### SetLowerRailPosition
Set the position of the lower rail (bottom-up).

```bash
curl -X PUT -H "BOND-Token: {token}" \
  -d '{"argument": 70}' \
  http://{ip}/v2/devices/{id}/actions/SetLowerRailPosition
```

### Notes

- The `SetPosition` action sets the upper rail to 0% and the lower rail to the requested position.
- If an action requests a position that would cause the rails to cross, the other rail is automatically adjusted to the minimum distance necessary. For example, if upper rail is at 50% and lower rail is at 75%, requesting upper rail at 80% will "push" the lower rail to 80% as well.
- To change both rails, call both actions in any order. Rail motions may be slightly staggered.

---

## SheerBlackoutDuo Feature

Dual-layer control for shades with both sheer and blackout fabric layers.

### State Variables

| Variable | Type | Description |
|----------|------|-------------|
| `blackout_position` | integer | 0 = open, 100 = closed |
| `sheer_position` | integer | 0 = open, 100 = closed |

### Actions

#### SetBlackoutPosition
Set the position of the blackout (opaque) layer.

```bash
curl -X PUT -H "BOND-Token: {token}" \
  -d '{"argument": 100}' \
  http://{ip}/v2/devices/{id}/actions/SetBlackoutPosition
```

#### SetSheerPosition
Set the position of the sheer (translucent) layer.

```bash
curl -X PUT -H "BOND-Token: {token}" \
  -d '{"argument": 50}' \
  http://{ip}/v2/devices/{id}/actions/SetSheerPosition
```

### Notes

- The `SetPosition` action sets the sheer layer to the requested position and the blackout layer to 0%.
- The two layers can often be positioned independently, but there may be constraints such as:
  - The blackout layer cannot be positioned below the sheer layer
  - The sheer layer must be fully extended before the blackout layer can extend
- These constraints are enforced by Bond Bridge automatically. If an impossible position is requested, the other layer is adjusted to the minimum necessary.
- To change both layers, call both actions in any order. Layer motions may be slightly staggered.

---

## State Variables Summary

| Variable | Feature | Type | Description |
|----------|---------|------|-------------|
| `open` | Open | integer | 1 = open, 0 = closed |
| `position` | Position | integer | 0 = open, 100 = closed |
| `tilt_position` | TiltPosition | integer | Angle in degrees |
| `upper_rail_position` | TDBU | integer | 0 = open, 100 = closed |
| `lower_rail_position` | TDBU | integer | 0 = open, 100 = closed |
| `blackout_position` | SheerBlackoutDuo | integer | 0 = open, 100 = closed |
| `sheer_position` | SheerBlackoutDuo | integer | 0 = open, 100 = closed |

---

## Properties Summary

| Property | Feature | Type | Description |
|----------|---------|------|-------------|
| `feature_position` | Position | boolean | Enable/disable position feature |
| `course_time` | CourseTime | integer | Travel time in ms for dead-reckoning |
| `min_tilt` | TiltPosition | integer | Minimum tilt angle (default 0) |
| `max_tilt` | TiltPosition | integer | Maximum tilt angle (default 90) |

---

## Pairing Actions

Most shade devices use pairing rather than remote cloning.

### Pair
Pair the Bond Bridge with a shade motor. Requires manually putting the shade into pairing mode first.

```bash
curl -X PUT -H "BOND-Token: {token}" http://{ip}/v2/devices/{id}/actions/Pair
```

### Unpair
Unpair the Bond Bridge from a shade motor. Requires manually putting the shade into pairing mode first.

```bash
curl -X PUT -H "BOND-Token: {token}" http://{ip}/v2/devices/{id}/actions/Unpair
```

### UnpairSelf
Unpair the Bond Bridge from all shades in range. Does not require pairing mode.

```bash
curl -X PUT -H "BOND-Token: {token}" http://{ip}/v2/devices/{id}/actions/UnpairSelf
```
