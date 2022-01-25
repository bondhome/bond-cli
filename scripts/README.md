# Scripts

Here you can find some useful scripts to automate tasks using the `bond-cli` tool.

## [add_multiple_devices.sh](add_multiple_devices.sh)
A script to add multiple copies of the same device. Useful for testing.

### Usage
```
Usage: ./scripts/add_multiple_devices.sh --bondID ZXBL00000 --deviceName 'Test Device' --location 'Bedroom' --template RMS12 --quantity 10
        --bondID The ID of the Bond you want to create the new devices
        --deviceName The name of the device. This will be a prefix of the actual name. I.e: 'Test Device 1', 'Test Device 2'...
        --location Device Location (Bedroom, Living Room, etc.)
        --template The device template name to be created (RCF84, A1, etc.)
        --quantity The amount of devices that will be created
```

### Example
```bash
# On the repository root folder
./scripts/add_multiple_devices.sh --bondID ZPEA12345 --deviceName "Test Shade" --location "Testing" --template RMS12 --quantity 15
```

That will create 15 RMS12 Motorized Shades starting with `Test Shade 01` through `Test Shade 15` in the `Testing` location.
So the final output would be:
```
Devices on ZPEA77140
----------------------------------------------------
|dev_id          |name            |location        |
|----------------|----------------|----------------|
|7c26c755c37a9d71|Test Shade 01   |Testing         |
|f27e84845e66cade|Test Shade 02   |Testing         |
|32a7a66bce293ca0|Test Shade 03   |Testing         |
|c0bbe6982a52dc24|Test Shade 04   |Testing         |
|b0d05e3ebefba5cd|Test Shade 05   |Testing         |
|d309f67257adffe1|Test Shade 06   |Testing         |
|fea75bbd5de7d783|Test Shade 07   |Testing         |
|c9da1d8bb323997a|Test Shade 08   |Testing         |
|7953e71d35873a80|Test Shade 09   |Testing         |
|adce5a30809542f7|Test Shade 10   |Testing         |
|0ffa61dd811639f3|Test Shade 11   |Testing         |
|c4b24e2a09c09ed4|Test Shade 12   |Testing         |
|3a4b45a6ea46d68a|Test Shade 13   |Testing         |
|0549cbd40147f4a6|Test Shade 14   |Testing         |
|827610a5e664e3e2|Test Shade 15   |Testing         |
----------------------------------------------------
Done!
```