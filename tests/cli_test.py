import pytest
import ouroboros.cli as cli
import ouroboros.defaults as defaults

def test_checkURI():
    assert cli.checkURI('tcp://0.0.0.0:1234')
    assert not cli.checkURI('tcp:/0.0.0.0')

def test_url_arg_invalid_value(mocker):
    mocker.patch('ouroboros.cli')
    cli.parser(['--url', 'tcp:/0.0.0.0:1234'])
    assert cli.host == defaults.LOCAL_UNIX_SOCKET

def test_url_arg_invalid_value(mocker):
    mocker.patch('ouroboros.cli')
    cli.parser(['--url', 'tcp:/0.0.0.0:1234'])
    assert cli.host == defaults.LOCAL_UNIX_SOCKET

def test_interval_arg_invalid_value(mocker):
    mocker.patch('ouroboros.cli')
    with pytest.raises(SystemExit) as pytest_wrapped_e:
            cli.parser(['--interval', 'test'])
            assert pytest_wrapped_e.type == SystemExit

def test_interval_arg_valid_value(mocker):
    mocker.patch('ouroboros.cli')
    assert cli.parser(['--interval', 0])
