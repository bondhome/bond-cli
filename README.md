[![PyPI version](https://badge.fury.io/py/bond-cli.svg)](https://badge.fury.io/py/bond-cli)

# Bond Command Line Interface

EDIT: This project is in a beta state. We released it on the principle of release early & often. It is here just in case it benefits a member of the Bond Home community. Your mileage may vary! Bug reports and feature requests are strongly encouraged, just open an issue!

## Purpose

This tool exists to make it easy to manipulate a Bond from a command line,
for use by:

 - Bond community
 - internal use in engineering and customer support

## Installation

Install with `pip install bond-cli`

## Getting Started

Find Bonds on local network:

```bash
bond discover
```

Check their firmware versions:

```bash
bond version
```

Select a Bond and set the token so we can go deeper:

```bash
bond select KX12345
bond token a938b2010cb203
```

List devices:

```bash
bond devices
```

## Injecting Devices

Create a template device:

```bash
bond device_create --name "Formidable Fan" --template A1 --addr 101 --freq 300000 --bps 1000 --zero_gap 1234
```

You can then see the fan on your Bond Home app.

## Live Logging

You can also start a livelog:

```bash
bond livelog --level info
```

## Upgrade Your Bond

You can upgrade your selected bond:

```bash
bond upgrade --release beta
```

## Getting Help

Get more help with:

```bash
bond -h
```
