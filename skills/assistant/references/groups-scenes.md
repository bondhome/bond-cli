# Groups and Scenes API Reference

## Overview

Groups and Scenes allow you to control multiple devices with a single command. Groups aggregate devices for simultaneous control, while Scenes define sequences of actions across devices and groups.

Both Groups and Scenes can span multiple Bonds (Bridges and SBB devices) by using the same ID (`_id` field) on each Bond.

---

## Groups

Groups are collections of Devices that can be controlled together. The available Actions on a Group are the intersection of Actions available on all member Devices.

### List Groups

```bash
curl -H "BOND-Token: $TOKEN" http://$BOND_IP/v2/groups
```

Response:
```json
{
  "_": "7fc1e84b",
  "3b20f300": { "_": "9a5e1136" },
  "4caf6472": { "_": "409d124b" }
}
```

### Create Group

```bash
curl -X POST -H "BOND-Token: $TOKEN" -H "Content-Type: application/json" \
  http://$BOND_IP/v2/groups \
  -d '{"name": "Kitchen Shades", "devices": ["aabbccdd", "11223344", "deadbeef"]}'
```

**Notes:**
- All devices must be compatible (have at least one common action)
- `types` and `locations` are auto-calculated from member devices
- For cross-Bond groups, provide a 64-bit `_id` field to use the same ID on each Bond

### Get Group

```bash
curl -H "BOND-Token: $TOKEN" http://$BOND_IP/v2/groups/{group_id}
```

Response:
```json
{
  "name": "Kitchen Shades",
  "devices": ["aabbccdd", "11223344", "deadbeef"],
  "types": ["MS"],
  "locations": ["Kitchen"],
  "actions": ["Open", "Close", "Preset"],
  "state": { "_": "ad9bcde4" }
}
```

### Update Group

```bash
curl -X PATCH -H "BOND-Token: $TOKEN" -H "Content-Type: application/json" \
  http://$BOND_IP/v2/groups/{group_id} \
  -d '{"name": "All Kitchen Shades"}'
```

Update device membership:
```bash
curl -X PATCH -H "BOND-Token: $TOKEN" -H "Content-Type: application/json" \
  http://$BOND_IP/v2/groups/{group_id} \
  -d '{"devices": ["aabbccdd", "11223344"]}'
```

**Note:** If the `devices` list is PATCHed to empty, the group is deleted.

### Delete Group

```bash
curl -X DELETE -H "BOND-Token: $TOKEN" http://$BOND_IP/v2/groups/{group_id}
```

### Execute Group Action

```bash
curl -X PUT -H "BOND-Token: $TOKEN" -H "Content-Type: application/json" \
  http://$BOND_IP/v2/groups/{group_id}/actions/{action_name} \
  -d '{}'
```

With argument:
```bash
curl -X PUT -H "BOND-Token: $TOKEN" -H "Content-Type: application/json" \
  http://$BOND_IP/v2/groups/{group_id}/actions/SetPosition \
  -d '{"argument": 50}'
```

**Notes:**
- Blocks until all member devices have executed (timeout max 7 seconds)
- Available actions come from the `actions` list in the Group response

### Get Group State

```bash
curl -H "BOND-Token: $TOKEN" http://$BOND_IP/v2/groups/{group_id}/state
```

Response:
```json
{
  "open": 1
}
```

### State Aggregation Behavior

Group State lists state variables common to all member Devices:
- If all members have the same value for a state variable, the Group shows that value
- If members differ, the Group variable shows `null`

Example: If 3 shades are in a group and 2 are open (`open: 1`) and 1 is closed (`open: 0`), the group state will be `{"open": null}`.

### Group Properties

Get properties common to all member devices:
```bash
curl -H "BOND-Token: $TOKEN" http://$BOND_IP/v2/groups/{group_id}/properties
```

Update properties on all members at once:
```bash
curl -X PATCH -H "BOND-Token: $TOKEN" -H "Content-Type: application/json" \
  http://$BOND_IP/v2/groups/{group_id}/properties \
  -d '{"feature_position": true}'
```

---

## Scenes

Scenes are sets of actions to run on Devices and/or Groups with a single request.

### List Scenes

```bash
curl -H "BOND-Token: $TOKEN" http://$BOND_IP/v2/scenes
```

Response:
```json
{
  "_": "7fc1e84b",
  "3b20f300": { "_": "9a5e1136" },
  "4caf6472": { "_": "409d124b" }
}
```

### Create Scene

```bash
curl -X POST -H "BOND-Token: $TOKEN" -H "Content-Type: application/json" \
  http://$BOND_IP/v2/scenes \
  -d '{
    "name": "Movie Mode",
    "actors": [
      {"device": "aabbccdd", "action": "TurnOff"},
      {"device": "11223344", "action": "SetBrightness", "argument": 20},
      {"group": "deadbeef", "action": "Close"}
    ]
  }'
```

### Actor Format

Each actor in the `actors` array specifies:

```json
{
  "device": "device_id",   // OR "group": "group_id"
  "action": "ActionName",
  "argument": <optional>   // For actions that take arguments
}
```

Examples:
```json
{"device": "aabbccdd", "action": "TurnOn"}
{"device": "11223344", "action": "SetSpeed", "argument": 3}
{"group": "deadbeef", "action": "SetBrightness", "argument": 50}
{"device": "cafebabe", "action": "SetPosition", "argument": 75}
```

### Get Scene

```bash
curl -H "BOND-Token: $TOKEN" http://$BOND_IP/v2/scenes/{scene_id}
```

Response:
```json
{
  "name": "Movie Mode",
  "actors": [
    {"device": "aabbccdd", "action": "TurnOff"},
    {"device": "11223344", "action": "SetBrightness", "argument": 20}
  ],
  "types": ["CF", "LT"],
  "locations": ["Living Room"]
}
```

### Update Scene

```bash
curl -X PATCH -H "BOND-Token: $TOKEN" -H "Content-Type: application/json" \
  http://$BOND_IP/v2/scenes/{scene_id} \
  -d '{"name": "Movie Night"}'
```

Update actors:
```bash
curl -X PATCH -H "BOND-Token: $TOKEN" -H "Content-Type: application/json" \
  http://$BOND_IP/v2/scenes/{scene_id} \
  -d '{
    "actors": [
      {"device": "aabbccdd", "action": "TurnOff"},
      {"device": "11223344", "action": "SetBrightness", "argument": 10}
    ]
  }'
```

**Note:** If the `actors` list is PATCHed to empty, the scene is deleted.

### Delete Scene

```bash
curl -X DELETE -H "BOND-Token: $TOKEN" http://$BOND_IP/v2/scenes/{scene_id}
```

### Run Scene

```bash
curl -X PUT -H "BOND-Token: $TOKEN" http://$BOND_IP/v2/scenes/{scene_id}/run
```

Each actor is executed individually when the scene runs.

---

## Cross-Bond Groups and Scenes

To create a Group or Scene that spans multiple Bonds:

1. Generate a unique 64-bit ID
2. Include the same `_id` field in each POST request to each Bond

```bash
# On Bond 1
curl -X POST -H "BOND-Token: $TOKEN1" -H "Content-Type: application/json" \
  http://$BOND1_IP/v2/groups \
  -d '{"_id": "mygroup123", "name": "All Shades", "devices": ["dev1", "dev2"]}'

# On Bond 2
curl -X POST -H "BOND-Token: $TOKEN2" -H "Content-Type: application/json" \
  http://$BOND2_IP/v2/groups \
  -d '{"_id": "mygroup123", "name": "All Shades", "devices": ["dev3", "dev4"]}'
```

---

## Use Case Examples

### Movie Mode

Dim lights, close shades, and turn on the TV backlight:

```bash
curl -X POST -H "BOND-Token: $TOKEN" -H "Content-Type: application/json" \
  http://$BOND_IP/v2/scenes \
  -d '{
    "name": "Movie Mode",
    "actors": [
      {"device": "living_light", "action": "SetBrightness", "argument": 10},
      {"group": "all_shades", "action": "Close"},
      {"device": "backlight", "action": "TurnOn"}
    ]
  }'
```

### Goodnight Scene

Turn off all lights and fans:

```bash
curl -X POST -H "BOND-Token: $TOKEN" -H "Content-Type: application/json" \
  http://$BOND_IP/v2/scenes \
  -d '{
    "name": "Goodnight",
    "actors": [
      {"group": "all_lights", "action": "TurnOff"},
      {"group": "all_fans", "action": "TurnOff"}
    ]
  }'
```

### All Off

Create a group of all controllable devices and turn them off:

```bash
# First create a group (if devices are compatible)
curl -X POST -H "BOND-Token: $TOKEN" -H "Content-Type: application/json" \
  http://$BOND_IP/v2/groups \
  -d '{"name": "Everything", "devices": ["dev1", "dev2", "dev3"]}'

# Execute TurnOff on the group
curl -X PUT -H "BOND-Token: $TOKEN" \
  http://$BOND_IP/v2/groups/{group_id}/actions/TurnOff \
  -d '{}'
```

Or use a scene for heterogeneous devices:

```bash
curl -X POST -H "BOND-Token: $TOKEN" -H "Content-Type: application/json" \
  http://$BOND_IP/v2/scenes \
  -d '{
    "name": "All Off",
    "actors": [
      {"device": "fan1", "action": "TurnOff"},
      {"device": "light1", "action": "TurnOff"},
      {"device": "shade1", "action": "Close"}
    ]
  }'
```

---

## API Summary

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List groups | GET | `/v2/groups` |
| Create group | POST | `/v2/groups` |
| Get group | GET | `/v2/groups/{id}` |
| Update group | PATCH | `/v2/groups/{id}` |
| Delete group | DELETE | `/v2/groups/{id}` |
| Execute group action | PUT | `/v2/groups/{id}/actions/{action}` |
| Get group state | GET | `/v2/groups/{id}/state` |
| Get group properties | GET | `/v2/groups/{id}/properties` |
| Update group properties | PATCH | `/v2/groups/{id}/properties` |
| List scenes | GET | `/v2/scenes` |
| Create scene | POST | `/v2/scenes` |
| Get scene | GET | `/v2/scenes/{id}` |
| Update scene | PATCH | `/v2/scenes/{id}` |
| Delete scene | DELETE | `/v2/scenes/{id}` |
| Run scene | PUT | `/v2/scenes/{id}/run` |
