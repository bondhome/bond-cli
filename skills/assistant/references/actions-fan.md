# Ceiling Fan Actions

Device type: `CF` (Ceiling Fan)

## Power

### Actions

| Action | Description | Argument |
|--------|-------------|----------|
| TurnOn | Turn fan on (resumes previous speed) | None |
| TurnOff | Turn fan off | None |
| TogglePower | Toggle fan on/off | None |

### State Variables

- `power`: 1 = on, 0 = off

### Examples

```bash
# Turn on
curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}/v2/devices/{id}/actions/TurnOn

# Turn off
curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}/v2/devices/{id}/actions/TurnOff
```

## Speed

### Properties

- `max_speed`: Maximum speed number (read-only)

### Actions

| Action | Description | Argument |
|--------|-------------|----------|
| SetSpeed | Set fan speed and turn on | 1 to max_speed |
| IncreaseSpeed | Increase speed by N | Number of steps |
| DecreaseSpeed | Decrease speed by N (won't go below 1) | Number of steps |

### State Variables

- `speed`: Current speed (1 to max_speed). If power=0, represents last speed.

### Examples

```bash
# Set speed to 3
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": 3}' \
  http://{ip}/v2/devices/{id}/actions/SetSpeed

# Increase speed by 1
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": 1}' \
  http://{ip}/v2/devices/{id}/actions/IncreaseSpeed

# Check max_speed
curl -H "BOND-Token: {token}" http://{ip}/v2/devices/{id}/properties
```

## Breeze

Randomized breeze mode that varies fan speed over time.

### Actions

| Action | Description | Argument |
|--------|-------------|----------|
| BreezeOn | Enable breeze with remembered params | None |
| BreezeOff | Disable breeze (fan stays at current speed) | None |
| SetBreeze | Enable breeze with specific params | [mode, mean, var] |

### State Variables

- `breeze`: Array `[mode, mean, var]`
  - `mode`: 0 = disabled, 1 = enabled
  - `mean`: Average speed (0-100, where 0=calm, 100=storm)
  - `var`: Variability (0-100, where 0=steady, 100=gusty)

### Examples

```bash
# Enable breeze
curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}/v2/devices/{id}/actions/BreezeOn

# Set custom breeze (mode=1, mean=30, var=80)
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": [1, 30, 80]}' \
  http://{ip}/v2/devices/{id}/actions/SetBreeze

# Disable breeze
curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}/v2/devices/{id}/actions/BreezeOff
```

## Direction

### Actions

| Action | Description | Argument |
|--------|-------------|----------|
| SetDirection | Set fan direction | 1 (forward/summer) or -1 (reverse/winter) |
| ToggleDirection | Reverse current direction | None |

### State Variables

- `direction`: 1 = forward (summer), -1 = reverse (winter)

### Examples

```bash
# Set to reverse (winter mode)
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": -1}' \
  http://{ip}/v2/devices/{id}/actions/SetDirection

# Toggle direction
curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}/v2/devices/{id}/actions/ToggleDirection
```

## Light

Basic light on/off control for fans with integrated lights.

### Properties

- `feature_light`: true/false - whether light feature is enabled

### Actions

| Action | Description | Argument |
|--------|-------------|----------|
| TurnLightOn | Turn light on | None |
| TurnLightOff | Turn light off | None |
| ToggleLight | Toggle light on/off | None |

### State Variables

- `light`: 1 = on, 0 = off

### Examples

```bash
# Turn light on
curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}/v2/devices/{id}/actions/TurnLightOn

# Turn light off
curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}/v2/devices/{id}/actions/TurnLightOff
```

## Up/Down Light

For fans with separate upward-facing and downward-facing lights.

### Properties

- `feature_up_down_light`: true/false - whether up/down light feature is enabled

### Actions

| Action | Description |
|--------|-------------|
| TurnUpLightOn | Turn up light on |
| TurnUpLightOff | Turn up light off |
| TurnDownLightOn | Turn down light on |
| TurnDownLightOff | Turn down light off |
| ToggleUpLight | Toggle up light |
| ToggleDownLight | Toggle down light |

### State Variables

- `up_light`: 1 = enabled, 0 = disabled
- `down_light`: 1 = enabled, 0 = disabled

The physical light is on when both `light=1` AND the respective `up_light`/`down_light=1`.

### Examples

```bash
# Turn on only down light
curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}/v2/devices/{id}/actions/TurnUpLightOff
curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}/v2/devices/{id}/actions/TurnDownLightOn
curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}/v2/devices/{id}/actions/TurnLightOn
```

## Brightness

For dimmable fan lights.

### Properties

- `feature_brightness`: true/false - whether brightness control is available

### Actions

| Action | Description | Argument |
|--------|-------------|----------|
| SetBrightness | Set brightness level | 1-100 (percent) |
| IncreaseBrightness | Increase brightness | Amount (percent) |
| DecreaseBrightness | Decrease brightness | Amount (percent) |

### State Variables

- `brightness`: 1-100 (percent). If light=0, represents remembered brightness.

### Examples

```bash
# Set brightness to 75%
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": 75}' \
  http://{ip}/v2/devices/{id}/actions/SetBrightness

# Increase brightness by 10%
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": 10}' \
  http://{ip}/v2/devices/{id}/actions/IncreaseBrightness
```

## Up/Down Brightness

For fans with separately dimmable up and down lights.

### Actions

| Action | Description | Argument |
|--------|-------------|----------|
| SetUpLightBrightness | Set up light brightness | 1-100 |
| SetDownLightBrightness | Set down light brightness | 1-100 |
| IncreaseUpLightBrightness | Increase up light brightness | Amount |
| IncreaseDownLightBrightness | Increase down light brightness | Amount |
| DecreaseUpLightBrightness | Decrease up light brightness | Amount |
| DecreaseDownLightBrightness | Decrease down light brightness | Amount |

### State Variables

- `up_light_brightness`: 1-100
- `down_light_brightness`: 1-100

## Timer

Auto-off timer for fans.

### Properties

- `default_auto_timer_s`: For heater devices, auto-timer duration in seconds

### Actions

| Action | Description | Argument |
|--------|-------------|----------|
| SetTimer | Start timer (turns on if off) | Seconds (0 to cancel) |

### State Variables

- `timer`: Seconds remaining, or 0 if no timer

### Examples

```bash
# Set 30 minute timer
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": 1800}' \
  http://{ip}/v2/devices/{id}/actions/SetTimer

# Cancel timer
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": 0}' \
  http://{ip}/v2/devices/{id}/actions/SetTimer
```

## Checking Properties

To see what features a fan supports:

```bash
curl -H "BOND-Token: {token}" http://{ip}/v2/devices/{id}/properties
```

Returns properties like `max_speed`, `feature_light`, `feature_brightness`, etc.
