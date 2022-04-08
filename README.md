[![PyPI version](https://badge.fury.io/py/bond-cli.svg)](https://badge.fury.io/py/bond-cli)

# Bond Command Line Interface

EDIT: This project is in a beta state. We released it on the principle of release early & often. It is here just in case it benefits a member of the Bond Home community. Your mileage may vary!

## Purpose

This tool exists to make it easy to manipulate a Bond from a command line,
for use by:

 - Bond community
 - internal use in engineering and customer support

## Installation

Install with

```bash
pip install bond-cli
```

## Getting Started

Find Bonds on local network:

```bash
bond discover
```


Select a Bond and set the token so we can go deeper:

```bash
bond select <your Bond's ID or a prefix>
```

If your Bond's token is unlocked, `select` will retrieve and store it. Otherwise, you have
a couple options. You can unlock the token yourself (a power cycle is the easiest way, it'll
be unlocked for a period after a reboot), and run the following to automatically retrieve
and store it:

```bash
bond token
```

Or, you can manually set the token, which you could find in the Bond Home app
in the Bond's settings screen.

```bash
bond token <your Bond's token>
```

Now that you've selected a Bond and stored its token, you're ready to interact with it.

Check its firmware version:

```bash
bond version
```

## Device Management

Create a template device:

```bash
bond devices create --name "Formidable Fan" --location "Bedroom" --template A1 --addr 101 --freq 300000 --bps 1000 --zero_gap 1234
```

You can then see the fan on your Bond Home app.

List existing devices:

```bash
bond devices list
```

Delete one or more devices:

```bash
bond devices delete <DEVICE1_ID> <DEVICE2_ID>
```

## Device Groups

Create a device group:

```bash
bond groups create --name "All Shades" <BOND1_ID>:<DEVICE1_ID> <BOND2_ID>:<DEVICE1_ID> <BOND2_ID>:<DEVICE2_ID> 
```

List the existing device groups:

```bash
bond groups list
```

List the device groups on a single Bond (may not represent the whole group):

```bash
bond groups list --bond-id <BOND_ID>
```

## Live Logging

You can also start a livelog:

```bash
bond livelog --level info
```

## Upgrade Your Bond

You can upgrade your selected bond:

```bash
bond upgrade beta
```

## Getting Help

Get more help with:

```bash
bond -h
```

or you can get help with any subcommand
```bash
bond select -h
```

## Contributing

Bug reports and feature requests in the form of issues and pull requests are strongly encouraged!

To develop locally, you can clone the repository from github, remove the package if already present, then install it to pip in local editable mode:

```bash
git clone git@github.com:bondhome/bond-cli.git
cd bond-cli
pip uninstall bond-cli
pip install -e "."
```

Now all changes made in your local copy of `bond-cli` will be reflected in the `bond` executable.

## Release Procedure

To make a release, bump the version number in `setup.py` on trunk, then make an annotated tag

```bash
git tag -a "v1.8.7"
```

with a version matching that in `setup.py`. You'll be prompted to write some release notes.
Alternatively, use the Github repository's releases interface to create a release.

Upon pushing the tag or publishing the release, CI will deploy to PyPi.
