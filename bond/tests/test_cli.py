import os


def test_help_os():
    result = os.system("bond --help")
    assert result == 0

    result = os.system("bond -h")
    assert result == 0


def test_no_args(script_runner, help_text):
    result = script_runner.run("bond")
    assert result.success
    assert result.stdout == help_text
    assert result.stderr == ""


def test_help(script_runner, help_text):
    result = script_runner.run("bond", "--help")
    assert result.success
    assert result.stdout == help_text
    assert result.stderr == ""

    result = script_runner.run("bond", "-h")
    assert result.success
    assert result.stdout == help_text
    assert result.stderr == ""


# def test_discover_command(script_runner, sleep_mock, discover_scanner_mock):
#     result = script_runner.run("bond", "discover")
#
#     expected_output = (
#         " -----------------------------------------------------------------\n"
#         "| bondid              | ip                  | port                | \n"
#         "| ------------------- | ------------------- | ------------------- | \n"
#     )
#
#     assert result.success
#     assert result.stdout == expected_output
#     assert result.stderr == ""


def test_list_command(script_runner, bond_db_mocks):
    result = script_runner.run("bond", "list")

    expected_output = (
        " -----------------------------------------------------------------\n"
        "| bondid              | ip                  | token               | \n"
        "| ------------------- | ------------------- | ------------------- | \n"
        "| ZPEA77129           | 192.168.1.12        | None                | \n"
        "| ZZDI37978 <-----    | 192.168.1.11        | 7a122aaa89393abc    | \n"
        " -----------------------------------------------------------------\n"
    )

    assert result.success
    assert result.stdout == expected_output
    assert result.stderr == ""


def test_select_command(script_runner, bond_db_mocks):
    result = script_runner.run("bond", "select")

    assert result.success
    assert result.stdout == "Bond selected: ZZDI37978\n"
    assert result.stderr == ""
