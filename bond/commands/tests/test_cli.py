import os

import pytest


@pytest.fixture
def no_sleep(mocker):
    return mocker.patch("time.sleep")


@pytest.fixture
def local_json_db(mocker):
    db_json = {
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

    json_load_mock = mocker.patch("json.load")
    json_load_mock.return_value = db_json


def test_help():
    result = os.system("bond --help")
    assert result == 0

    result = os.system("bond --h")
    assert result == 0


def test_discover_command(script_runner, no_sleep):
    ret = script_runner.run("bond", "discover")

    expected_output = """----------------------------------------------------------------
|bondid              |ip                  |port                |
|--------------------|--------------------|--------------------|
"""

    assert ret.success
    assert ret.stdout == expected_output
    assert ret.stderr == ""


def test_list_command(script_runner, local_json_db):
    ret = script_runner.run("bond", "list")

    expected_output = """----------------------------------------------------------------
|bondid              |ip                  |token               |
|--------------------|--------------------|--------------------|
|ZPEA77129           |192.168.1.12        |None                |
|ZZDI37978           |192.168.1.11        |7a122aaa89393abc    |
----------------------------------------------------------------
"""

    assert ret.success
    assert ret.stdout == expected_output
    assert ret.stderr == ""


def test_select_command(script_runner, local_json_db):
    ret = script_runner.run("bond", "select")

    assert ret.success
    assert ret.stdout == "Bond selected: ZZDI37978\n"
    assert ret.stderr == ""
