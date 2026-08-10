# RF/IR Signals Reference

> **Bridge-only feature**: Signal transmission and scanning are only available on Bond Bridge devices.

> **Note**: This is advanced/developer territory. Most users will not need to interact with signals directly.

## Signal Schema

A signal object contains the following fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `freq` | number | Yes | Frequency in kHz |
| `modulation` | string | No | `OOK` (on-off keying) or `GFSK` (gaussian frequency-shift keying). Default: `OOK` |
| `encoding` | string | Yes | Data encoding: `cq` or `hex` |
| `bps` | number | Yes | Bitrate (100-40000) |
| `data` | string | Yes | Encoded signal data (max 6144 bytes) |
| `reps` | number | No | Number of repetitions. Default: `1` |

## Frequency

The `freq` field determines whether the signal is RF or IR:

- **RF**: `freq >= 1000` (e.g., `434000` for 434 MHz, `350000` for 350 MHz)
- **IR**: `freq < 1000` (e.g., `38` for 38 kHz infrared)

Bond Bridge receives and transmits IR signals at 38 kHz.

## Encoding Types

### CQ Encoding (`"cq"`)

A simple encoding where bits are represented using characters:

- `0` - single zero bit
- `1` - single one bit
- `C` through `Q` - 2^0 (1) through 2^14 (16384) zero bits
- `c` through `q` - 2^0 (1) through 2^14 (16384) one bits
- `A` - the three bits `110`
- `B` - the three bits `011`

### Hex Encoding (`"hex"`)

Each hex byte represents 8 bits of data. Currently limited to 40000 bps only.

This is the default encoding for scan results.

## API Endpoints

### Transmit a Signal

```bash
curl -X PUT "http://<bond-ip>/v2/signal/tx" \
  -H "BOND-Token: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "freq": 434000,
    "modulation": "OOK",
    "encoding": "cq",
    "bps": 1000,
    "data": "110100110110H",
    "reps": 12
  }'
```

### Scan for Signals

Start a scan on a specific frequency:

```bash
curl -X PUT "http://<bond-ip>/v2/signal/scan" \
  -H "BOND-Token: <token>" \
  -H "Content-Type: application/json" \
  -d '{"freq": 434000}'
```

To scan IR instead:

```bash
curl -X PUT "http://<bond-ip>/v2/signal/scan" \
  -H "BOND-Token: <token>" \
  -H "Content-Type: application/json" \
  -d '{"freq": 38}'
```

### Get Scan Result

Retrieve the signal captured by the most recent scan:

```bash
curl -X GET "http://<bond-ip>/v2/signal/scan/signal" \
  -H "BOND-Token: <token>"
```

### Transmit Last Scanned Signal

Transmit the signal that was just scanned:

```bash
curl -X PUT "http://<bond-ip>/v2/signal/tx" \
  -H "BOND-Token: <token>" \
  -H "Content-Type: application/json" \
  -d '{"use_scan": true}'
```

### Cancel Transmission

```bash
curl -X DELETE "http://<bond-ip>/v2/signal/tx" \
  -H "BOND-Token: <token>"
```

## Command Signals

Signals can be associated with device commands.

### Get Command Signal

```bash
curl -X GET "http://<bond-ip>/v2/devices/<device_id>/commands/<command_id>/signal" \
  -H "BOND-Token: <token>"
```

### Set Command Signal

```bash
curl -X PUT "http://<bond-ip>/v2/devices/<device_id>/commands/<command_id>/signal" \
  -H "BOND-Token: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "freq": 434000,
    "encoding": "cq",
    "bps": 1000,
    "data": "110100110110H"
  }'
```

### Transmit Command Signal

Transmit the signal associated with a command (does not execute the action or update device state):

```bash
curl -X PUT "http://<bond-ip>/v2/devices/<device_id>/commands/<command_id>/tx" \
  -H "BOND-Token: <token>" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## RSSI Sweep

Get Receive Signal Strength Indication across the frequency range (useful for antenna tuning):

```bash
curl -X GET "http://<bond-ip>/v2/signal/rssi" \
  -H "BOND-Token: <token>"
```

Response format:

```json
{
  "format": ["freq", "rssi"],
  "results": [
    [350000, 80],
    [351000, 87],
    [352000, 92]
  ]
}
```
