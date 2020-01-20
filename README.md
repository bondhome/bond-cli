# Bond Command Line Interface

EDIT: This project is in an ALPHA state. We released it on the principle of release early & often. However, we cannot support this code in its current state, and it is not being actively developed. It is here just in case it benefits a member of the Bond Home community. Your mileage may vary!

## Purpose

This tool exists to make it easy to manipulate a Bond from a command line,
for use by:

 - Bond community
 - internal use in engineering and customer support

## Requirements

This project uses `Python 3`, so make sure you are not using `Python 2.7`.
Also make sure you are using `pip` >= 3

You will need to first install the required packages:

```bash
pip3 install -r bond/requirements.txt
```

## Getting Started

Find Bonds on local network:

```bash
python3 -m bond discover
```

Check their firmware versions:

```bash
python3 -m bond version
```

Select a Bond and set the token so we can go deeper:

```bash
python3 -m bond select KX12345
python3 -m bond token a938b2010cb203
```

List devices:

```bash
python3 -m bond devices
```

## Injecting Devices

Create a template device:

```bash
python3 -m bond device_create --name "Formidable Fan" --template A1 --addr 101 --freq 300000 --bps 1000 --zero_gap 1234
```

You can then see the fan on your Bond Home app.

## Live Logging

You can also start a livelog:

```bash
python3 -m bond livelog --info
```

## Getting Help

Get more help with:

```bash
python3 -m bond -h
```
