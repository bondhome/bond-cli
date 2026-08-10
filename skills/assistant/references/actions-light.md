# Light Actions Reference

Device type: `LT` (Light)

This document covers standalone light devices. For fan lights (using TurnLightOn, TurnLightOff, etc.), see `actions-fan.md`.

## Power Feature

Controls the basic on/off state of the light.

### State Variables

- **power**: (integer) 1 = on, 0 = off

### Actions

| Action | Description |
|--------|-------------|
| TurnOn | Turn the light on |
| TurnOff | Turn the light off |
| TogglePower | Toggle power state (on to off, or off to on) |

### Curl Examples

```bash
# Turn on
curl -X PUT -H "BOND-Token: {token}" -H "Content-Type: application/json" \
  http://{ip}/v2/devices/{id}/actions/TurnOn

# Turn off
curl -X PUT -H "BOND-Token: {token}" -H "Content-Type: application/json" \
  http://{ip}/v2/devices/{id}/actions/TurnOff

# Toggle power
curl -X PUT -H "BOND-Token: {token}" -H "Content-Type: application/json" \
  http://{ip}/v2/devices/{id}/actions/TogglePower
```

## Brightness Feature

Controls dimmable lights with adjustable brightness levels.

### State Variables

- **brightness**: (integer) Percentage value 1-100. When light is off, represents the last brightness setting and the brightness to resume when turned on.

### Actions

| Action | Argument | Description |
|--------|----------|-------------|
| SetBrightness | 1-100 | Set brightness to specified percentage. Value of 0 is ignored; use TurnOff instead. |
| IncreaseBrightness | amount | Increase brightness by specified percentage. Turns on light if off. |
| DecreaseBrightness | amount | Decrease brightness by specified percentage. Minimum is 1%. Light remains off if already off. |

### Curl Examples

```bash
# Set brightness to 75%
curl -X PUT -H "BOND-Token: {token}" -H "Content-Type: application/json" \
  -d '{"argument": 75}' \
  http://{ip}/v2/devices/{id}/actions/SetBrightness

# Increase brightness by 10%
curl -X PUT -H "BOND-Token: {token}" -H "Content-Type: application/json" \
  -d '{"argument": 10}' \
  http://{ip}/v2/devices/{id}/actions/IncreaseBrightness

# Decrease brightness by 10%
curl -X PUT -H "BOND-Token: {token}" -H "Content-Type: application/json" \
  -d '{"argument": 10}' \
  http://{ip}/v2/devices/{id}/actions/DecreaseBrightness
```

## ColorTemp Feature

Controls correlated color temperature (CCT) of lights that support it.

Color temperature works in 100 Kelvin (K) steps. Non-multiples of 100 K will be rounded.

### Properties

- **min_color_temp**: (integer) Minimum color temperature in Kelvin
- **max_color_temp**: (integer) Maximum color temperature in Kelvin

### State Variables

- **color_temp**: (integer) Color temperature in Kelvin (resolution: 100 K)

### Actions

| Action | Argument | Description |
|--------|----------|-------------|
| SetColorTemp | Kelvin value | Set color temperature. Implicitly turns light on. |
| IncreaseColorTemp | degrees K | Increase color temperature by specified degrees. Implicitly turns light on. |
| DecreaseColorTemp | degrees K | Decrease color temperature by specified degrees. Implicitly turns light on. |

### Curl Examples

```bash
# Set color temperature to 4000K (neutral white)
curl -X PUT -H "BOND-Token: {token}" -H "Content-Type: application/json" \
  -d '{"argument": 4000}' \
  http://{ip}/v2/devices/{id}/actions/SetColorTemp

# Increase color temperature by 500K (cooler/bluer)
curl -X PUT -H "BOND-Token: {token}" -H "Content-Type: application/json" \
  -d '{"argument": 500}' \
  http://{ip}/v2/devices/{id}/actions/IncreaseColorTemp

# Decrease color temperature by 500K (warmer/yellower)
curl -X PUT -H "BOND-Token: {token}" -H "Content-Type: application/json" \
  -d '{"argument": 500}' \
  http://{ip}/v2/devices/{id}/actions/DecreaseColorTemp
```

## Color Feature (RGB)

Controls full color lighting products using RGB color space.

### State Variables

- **rgb**: (object) Apparent color with keys:
  - `r`: (0-255) Red value
  - `g`: (0-255) Green value
  - `b`: (0-255) Blue value

### Actions

| Action | Argument | Description |
|--------|----------|-------------|
| SetRGB | {r, g, b} | Set color by RGB values (0-255 each). Partial specification allowed. Implicitly turns light on. |

### Curl Examples

```bash
# Set color to red
curl -X PUT -H "BOND-Token: {token}" -H "Content-Type: application/json" \
  -d '{"argument": {"r": 255, "g": 0, "b": 0}}' \
  http://{ip}/v2/devices/{id}/actions/SetRGB

# Set color to purple
curl -X PUT -H "BOND-Token: {token}" -H "Content-Type: application/json" \
  -d '{"argument": {"r": 128, "g": 0, "b": 255}}' \
  http://{ip}/v2/devices/{id}/actions/SetRGB

# Adjust only red channel (leaves g and b unchanged)
curl -X PUT -H "BOND-Token: {token}" -H "Content-Type: application/json" \
  -d '{"argument": {"r": 200}}' \
  http://{ip}/v2/devices/{id}/actions/SetRGB
```

## Color Feature (HSV)

Controls full color lighting products using HSV color space.

### State Variables

- **hsv**: (object) Apparent color with keys:
  - `h`: (0-359) Hue in degrees
  - `s`: (0-100) Saturation percentage
  - `v`: (0-100) Value/brightness percentage (same as `brightness` state variable)

### Actions

| Action | Argument | Description |
|--------|----------|-------------|
| SetHSV | {h, s, v} | Set color by HSV values. Partial specification allowed. Implicitly turns light on. |

### Curl Examples

```bash
# Set to fully saturated blue (hue 240)
curl -X PUT -H "BOND-Token: {token}" -H "Content-Type: application/json" \
  -d '{"argument": {"h": 240, "s": 100, "v": 100}}' \
  http://{ip}/v2/devices/{id}/actions/SetHSV

# Set hue and saturation only (leave brightness unchanged)
curl -X PUT -H "BOND-Token: {token}" -H "Content-Type: application/json" \
  -d '{"argument": {"h": 120, "s": 80}}' \
  http://{ip}/v2/devices/{id}/actions/SetHSV

# Set hue only (for color wheel interface)
curl -X PUT -H "BOND-Token: {token}" -H "Content-Type: application/json" \
  -d '{"argument": {"h": 60}}' \
  http://{ip}/v2/devices/{id}/actions/SetHSV
```

## RGBW Feature

For lights with four-channel LEDs (separate white channel).

When saturation (S) is zero, only the W channel is used. When S is non-zero, only RGB channels are used.

### State Variables

- **rgbw**: (object) Low-level LED channel values:
  - `r`: (0-255) Red channel
  - `g`: (0-255) Green channel
  - `b`: (0-255) Blue channel
  - `w`: (0-255) White channel

### Actions

| Action | Argument | Description |
|--------|----------|-------------|
| SetRGBW | {r, g, b, w} | Set low-level LED channel values (0-255 each). Allows combinations unreachable with SetRGB. Implicitly turns light on. |

### Curl Examples

```bash
# Set warm white only
curl -X PUT -H "BOND-Token: {token}" -H "Content-Type: application/json" \
  -d '{"argument": {"r": 0, "g": 0, "b": 0, "w": 255}}' \
  http://{ip}/v2/devices/{id}/actions/SetRGBW

# Mix red with white for warm red
curl -X PUT -H "BOND-Token: {token}" -H "Content-Type: application/json" \
  -d '{"argument": {"r": 200, "g": 0, "b": 0, "w": 100}}' \
  http://{ip}/v2/devices/{id}/actions/SetRGBW

# Full RGBW combination
curl -X PUT -H "BOND-Token: {token}" -H "Content-Type: application/json" \
  -d '{"argument": {"r": 100, "g": 50, "b": 150, "w": 75}}' \
  http://{ip}/v2/devices/{id}/actions/SetRGBW
```

## Reading Device State

To read the current state of any light:

```bash
curl -H "BOND-Token: {token}" http://{ip}/v2/devices/{id}/state
```

Example response for an RGBW light:

```json
{
  "power": 1,
  "brightness": 75,
  "color_temp": 4000,
  "rgb": {"r": 255, "g": 200, "b": 150},
  "hsv": {"h": 30, "s": 41, "v": 100},
  "rgbw": {"r": 255, "g": 200, "b": 150, "w": 0},
  "_": "abcd1234"
}
```
