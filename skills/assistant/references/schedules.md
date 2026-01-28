# Bond Schedules (Skeds) API Reference

## Endpoints

### Device Schedules
- `GET /v2/devices/{device_id}/skeds` - List all schedules for a device
- `POST /v2/devices/{device_id}/skeds` - Create a new schedule for a device
- `GET /v2/devices/{device_id}/skeds/{sked_id}` - Get a specific schedule
- `PATCH /v2/devices/{device_id}/skeds/{sked_id}` - Modify an existing schedule
- `DELETE /v2/devices/{device_id}/skeds/{sked_id}` - Delete a schedule

### Group Schedules
- `GET /v2/groups/{group_id}/skeds` - List all schedules for a group
- `POST /v2/groups/{group_id}/skeds` - Create a new schedule for a group

### Scene Schedules
- `GET /v2/scenes/{scene_id}/skeds` - List all schedules for a scene
- `POST /v2/scenes/{scene_id}/skeds` - Create a new schedule for a scene

Note: For scenes, the `action` field must not be set (the scene itself defines the action).

## Schedule Structure

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | string | Yes* | Action to execute (e.g., `TurnOn`, `SetBrightness`). *Not set for scene schedules. |
| `argument` | any | No | Argument for the action, if needed (e.g., brightness level 80) |
| `mark` | string | Yes | Time reference: `midnight`, `sunrise`, `sunset`, `dawn`, `dusk` |
| `seconds` | integer | Yes | Offset from mark in seconds. Negative = before, positive = after. |
| `days_of_week` | array | Yes | 7-element boolean array `[Sun, Mon, Tue, Wed, Thu, Fri, Sat]` |
| `enabled` | boolean | No | Whether schedule is active. Defaults to `true`. |

### Mark Values

- **midnight**: `seconds` is time since midnight in local timezone
- **sunrise**: `seconds` is offset from calculated local sunrise
- **sunset**: `seconds` is offset from calculated local sunset
- **dawn**: `seconds` is offset from civil dawn (sun 6 degrees below horizon, before sunrise)
- **dusk**: `seconds` is offset from civil dusk (sun 6 degrees below horizon, after sunset)

### Days of Week

Array of 7 booleans: `[Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday]`

Examples:
- Every day: `[true, true, true, true, true, true, true]`
- Weekdays only: `[false, true, true, true, true, true, false]`
- Weekends only: `[true, false, false, false, false, false, true]`

## Requirements for Solar Events

Solar-based marks (`sunrise`, `sunset`, `dawn`, `dusk`) require timezone and location to be configured.

### Setting Time and Location

```bash
# Set timezone and grid locator for solar calculations
curl -X PATCH "http://$BOND_IP/v2/sys/time" \
  -H "BOND-Token: $TOKEN" \
  -d '{"tz": "America/New_York", "grid": "FN31pr"}'
```

The `grid` field uses the Maidenhead Locator System (ham radio grid squares) for latitude/longitude.

### Error Conditions

A 400 error will result if:
- `mark` is `midnight` but `sys/time.tz` is `null`
- `mark` is `dawn`, `dusk`, `sunrise`, or `sunset` but `sys/time.grid` or `sys/time.tz` is `null`

## One-Shot Schedules

Setting all `days_of_week` to `false` creates a one-shot schedule that:
1. Executes exactly once at the next occurrence
2. Automatically sets `enabled` to `false` after executing

This is useful for "run once" operations like delayed actions.

## Curl Examples

### List Schedules for a Device

```bash
curl "http://$BOND_IP/v2/devices/$DEVICE_ID/skeds" \
  -H "BOND-Token: $TOKEN"
```

### Create a Schedule (Turn on at sunset)

```bash
curl -X POST "http://$BOND_IP/v2/devices/$DEVICE_ID/skeds" \
  -H "BOND-Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "TurnOn",
    "mark": "sunset",
    "seconds": 0,
    "days_of_week": [true, true, true, true, true, true, true]
  }'
```

### Create a Schedule (Turn off at 11 PM)

```bash
# 11 PM = 23 * 3600 = 82800 seconds after midnight
curl -X POST "http://$BOND_IP/v2/devices/$DEVICE_ID/skeds" \
  -H "BOND-Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "TurnOff",
    "mark": "midnight",
    "seconds": 82800,
    "days_of_week": [true, true, true, true, true, true, true]
  }'
```

### Create a Schedule (Dim to 50% at dusk, weekdays only)

```bash
curl -X POST "http://$BOND_IP/v2/devices/$DEVICE_ID/skeds" \
  -H "BOND-Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "SetBrightness",
    "argument": 50,
    "mark": "dusk",
    "seconds": 0,
    "days_of_week": [false, true, true, true, true, true, false]
  }'
```

### Create a One-Shot Schedule (Turn on in 30 minutes)

```bash
# Calculate seconds from current time to desired time
# For a one-shot, you need to calculate seconds from midnight to desired time
curl -X POST "http://$BOND_IP/v2/devices/$DEVICE_ID/skeds" \
  -H "BOND-Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "TurnOn",
    "mark": "midnight",
    "seconds": 54000,
    "days_of_week": [false, false, false, false, false, false, false]
  }'
```

### Get a Specific Schedule

```bash
curl "http://$BOND_IP/v2/devices/$DEVICE_ID/skeds/$SKED_ID" \
  -H "BOND-Token: $TOKEN"
```

### Update a Schedule (Disable it)

```bash
curl -X PATCH "http://$BOND_IP/v2/devices/$DEVICE_ID/skeds/$SKED_ID" \
  -H "BOND-Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"enabled": false}'
```

### Update a Schedule (Change time to 30 minutes before sunset)

```bash
curl -X PATCH "http://$BOND_IP/v2/devices/$DEVICE_ID/skeds/$SKED_ID" \
  -H "BOND-Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"seconds": -1800}'
```

### Delete a Schedule

```bash
curl -X DELETE "http://$BOND_IP/v2/devices/$DEVICE_ID/skeds/$SKED_ID" \
  -H "BOND-Token: $TOKEN"
```

## Notes

- Arctic Circle users: Solar-based schedules may not execute during periods around the solstices when sunrise/sunset do not occur.
- Schedule list responses use hash trees for efficient synchronization (see Hash Tree documentation).
- For Channel schedules (MT-1500), common actions include: `Raise`, `Lower`, `Stop`, `SetPosition`, `Preset`, `TurnLightOn`, `TurnLightOff`, `SetBrightness`. Note that `Open`/`Close` are not available for channel schedules.
