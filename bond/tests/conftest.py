import pytest


@pytest.fixture
def sleep_mock(mocker):
    return mocker.patch("time.sleep")


@pytest.fixture()
def mock_db():
    return {
        "bonds": {
            "ZPEA77129": {"ip": "192.168.1.12", "port": 80},
            "ZZDI37978": {
                "ip": "192.168.1.11",
                "port": 80,
                "token": "7a122aaa89393abc",
            },
        },
        "test": 4,
        "selected_bondid": "ZZDI37978",
    }


@pytest.fixture
def bond_db_mocks(mocker, mock_db):
    db_get_mock = mocker.patch("bond.database.BondDatabase.get")
    db_get_mock.side_effect = lambda key: mock_db.get(key)

    db_setdefault_mock = mocker.patch("bond.database.BondDatabase.setdefault")
    db_setdefault_mock.side_effect = lambda key, default: mock_db.get(key, default)

    return db_get_mock, db_setdefault_mock


@pytest.fixture
def discover_scanner_mock(mocker):
    scanner_mock = mocker.patch("bond.commands.discover.Scanner")
    scanner_mock.return_value = None
    return scanner_mock


@pytest.fixture()
def help_text():
    return (
        "usage: bond [-h]\n"
        "            {discover,select,version,token,list,devices,groups,livelog,signal,reset,reboot,wifi,upgrade,rfman,backup,restore}\n"
        "            ...\n"
        "\n"
        "positional arguments:\n"
        "  {discover,select,version,token,list,devices,groups,livelog,signal,reset,reboot,wifi,upgrade,rfman,backup,restore}\n"
        "    discover            Discover Bonds on local network.\n"
        "    select              Select a single Bond to interact with, If the token of\n"
        "                        this Bond is unlocked, it will be set. (The easiest\n"
        "                        way to unlock a token is with a power cycle)\n"
        "    version             Get firmware version and target of the selected Bond.\n"
        "    token               Manage token-based authentication.\n"
        "    list                List Bonds in local database.\n"
        "    devices             Interact with the selected Bond's devices.\n"
        "    groups              Interact with device groups.\n"
        "    livelog             Start streaming logs\n"
        "    signal              Transmit a signal. [Bridge only]\n"
        "    reset               Reset a Bond to set it up again on WiFi, clear its\n"
        "                        database, or reset its firmware to a rescue image\n"
        "    reboot              Reboot a Bond. No reset is performed.\n"
        "    wifi                Interact with Bond's wifi\n"
        "    upgrade             Upgrade your Bond. Choose either a released firmware\n"
        "                        or a firmware from a specific branch\n"
        "    rfman               Configure the RF Manager [Bridge Only]\n"
        "    backup              Backup a Bond\n"
        "    restore             Restore a Bond.\n"
        "\n"
        "options:\n"
        "  -h, --help            show this help message and exit\n"
    )
