# Bond Command Line Interface

## Purpose

This tool exists to make it easy to manipulate a Bond from a command line,
for use by:

 - Bond community
 - internal use in engineering and customer support

## Getting Started

Find Bonds on local network:

```
python -m bond discover
```

Check their firmware versions:

```
python -m bond version
```

Select a Bond and set the token so we can go deeper:

```
python -m bond select KX12345
python -m bond token a938b2010cb203
```

List devices:

```
python -m bond devices
```

## Injecting Devices

Create a template device:

```
python -m bond device_create --name "Formidable Fan" --template A1 --addr 101 --freq 300000 --bps 1000 --zero_gap 1234
```

You can then see the fan on your Bond Home app.

## Live Logging

You can also start a livelog:

```
python -m bond livelog --info
```

## Getting Help

Get more help with:

```
python -m bond -h
```
