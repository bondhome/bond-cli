# Fireplace and Heater Actions

Device types: `FP` (Fireplace), `HT` (Heater)

## Power

### Actions

| Action | Description | Argument |
|--------|-------------|----------|
| TurnOn | Turn device on (resumes previous flame/heat level) | None |
| TurnOff | Turn device off | None |
| TogglePower | Toggle device on/off | None |

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

## Flame

Controls the flame level for fireplaces.

### Actions

| Action | Description | Argument |
|--------|-------------|----------|
| SetFlame | Set flame level and turn on | 1-100 |
| IncreaseFlame | Increase flame level | Amount |
| DecreaseFlame | Decrease flame level (won't go below 1) | Amount |

### State Variables

- `flame`: 1-100. If power=0, represents last flame setting.

### Examples

```bash
# Set flame to 75%
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": 75}' \
  http://{ip}/v2/devices/{id}/actions/SetFlame

# Increase flame by 10
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": 10}' \
  http://{ip}/v2/devices/{id}/actions/IncreaseFlame

# Decrease flame by 10
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": 10}' \
  http://{ip}/v2/devices/{id}/actions/DecreaseFlame
```

## Heat

Controls the heat level for heaters and some fireplaces.

### Properties

- `feature_heat`: true/false - whether heat control is enabled (PATCH-able)

### Actions

| Action | Description | Argument |
|--------|-------------|----------|
| SetHeat | Set heat level and turn on | 1-100 |
| IncreaseHeat | Increase heat level | Amount |
| DecreaseHeat | Decrease heat level (won't go below 1) | Amount |
| HeatPresetNext | Jump to next preset heat value | None |
| HeatPresetPrev | Jump to previous preset heat value | None |

### State Variables

- `heat`: 1-100. If power=0, represents last heat setting.

### Examples

```bash
# Set heat to 50%
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": 50}' \
  http://{ip}/v2/devices/{id}/actions/SetHeat

# Increase heat by 20
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": 20}' \
  http://{ip}/v2/devices/{id}/actions/IncreaseHeat

# Decrease heat by 20
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": 20}' \
  http://{ip}/v2/devices/{id}/actions/DecreaseHeat

# Cycle to next preset
curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}/v2/devices/{id}/actions/HeatPresetNext

# Cycle to previous preset
curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}/v2/devices/{id}/actions/HeatPresetPrev
```

## Fireplace Fan (FpFan)

Controls a fireplace's built-in fan. This is independent of the Power feature (which controls the flame).

### Actions

| Action | Description | Argument |
|--------|-------------|----------|
| TurnFpFanOn | Turn fireplace fan on (restores previous speed) | None |
| TurnFpFanOff | Turn fireplace fan off | None |
| SetFpFan | Set fireplace fan speed | 1-100 |

### State Variables

- `fpfan_power`: 1 = on, 0 = off
- `fpfan_speed`: 1-100

### Examples

```bash
# Turn fireplace fan on
curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}/v2/devices/{id}/actions/TurnFpFanOn

# Turn fireplace fan off
curl -X PUT -H "BOND-Token: {token}" \
  http://{ip}/v2/devices/{id}/actions/TurnFpFanOff

# Set fireplace fan speed to 60%
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": 60}' \
  http://{ip}/v2/devices/{id}/actions/SetFpFan
```

## Timer

Auto-off timer for fireplaces and heaters.

### Properties

- `default_auto_timer_s`: (Heaters only) Auto-timer duration in seconds. When present, the timer starts automatically whenever Power is activated and resets on any state-changing action. The timer cannot exceed this value. This ensures fire code compliance (commonly 2 hours for heaters).

### Actions

| Action | Description | Argument |
|--------|-------------|----------|
| SetTimer | Start timer (turns on if off) | Seconds (0 to cancel) |

### State Variables

- `timer`: Seconds remaining, or 0 if no timer

### Examples

```bash
# Set 1 hour timer
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": 3600}' \
  http://{ip}/v2/devices/{id}/actions/SetTimer

# Set 30 minute timer
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": 1800}' \
  http://{ip}/v2/devices/{id}/actions/SetTimer

# Cancel timer (device stays on)
curl -X PUT -H "BOND-Token: {token}" \
  -H "Content-Type: application/json" \
  -d '{"argument": 0}' \
  http://{ip}/v2/devices/{id}/actions/SetTimer
```

### Timer Notes

- Timer is canceled by most Power/Speed actions (except TurnOn)
- When timer reaches zero, device turns off automatically
- For heaters with `default_auto_timer_s`, the timer auto-starts on power-on and resets on any state change

## Checking Properties

To see what features a fireplace or heater supports:

```bash
curl -H "BOND-Token: {token}" http://{ip}/v2/devices/{id}/properties
```

Returns properties like `feature_heat`, `default_auto_timer_s`, etc.

## State Variables Summary

| Variable | Description |
|----------|-------------|
| `power` | 1 = on, 0 = off |
| `flame` | Flame level 1-100 (Fireplace) |
| `heat` | Heat level 1-100 (Heater) |
| `fpfan_power` | Fireplace fan: 1 = on, 0 = off |
| `fpfan_speed` | Fireplace fan speed 1-100 |
| `timer` | Seconds remaining on timer, 0 = no timer |
