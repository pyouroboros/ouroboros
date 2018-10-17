import pytest
import ouroboros.cli as cli
import ouroboros.defaults as defaults

def test_checkURI():
    assert cli.checkURI('tcp://0.0.0.0:1234')
    assert not cli.checkURI('tcp:/0.0.0.0')


# URL
@pytest.mark.parametrize('url_args, url_result', [
    # Invalid regex
    (['-u', 'tcp:/0.0.0.0:1234'], defaults.LOCAL_UNIX_SOCKET),
    (['--url', 'tcp:/0.0.0.0:1234'], defaults.LOCAL_UNIX_SOCKET),
    # If none supplied, default to unix://
    (['-u', ''], defaults.LOCAL_UNIX_SOCKET),
    (['--url', ''], defaults.LOCAL_UNIX_SOCKET),
    # Valid Regex
    (['-u', 'tcp://0.0.0.0:1234'], 'tcp://0.0.0.0:1234'),
    (['--url', 'tcp://0.0.0.0:1234'], 'tcp://0.0.0.0:1234')
])

def test_url_args(mocker, url_args, url_result):
    mocker.patch('ouroboros.cli')
    cli.parser(url_args)
    assert cli.host == url_result

# Interval
@pytest.mark.parametrize('interval_env, interval_env_result', [
    ({'INTERVAL': 't'}, False),
    ({'INTERVAL': '10'}, 10),
])

def test_get_interval_env(mocker, interval_env, interval_env_result):
    mocker.patch.dict('os.environ', interval_env)
    assert cli.get_interval_env() == interval_env_result

def test_interval_arg_invalid_value(mocker):
    mocker.patch('ouroboros.cli')
    with pytest.raises(SystemExit) as pytest_wrapped_e:
            cli.parser(['--interval', 'test'])
            assert pytest_wrapped_e.type == SystemExit

def test_interval_arg_valid_value(mocker):
    mocker.patch('ouroboros.cli')
    assert cli.parser(['--interval', 0])

# Monitor
@pytest.mark.parametrize('monitor_args, monitor_result', [
    (['-m', 'test1', 'test2', 'test3'], ['test1', 'test2', 'test3']),
    (['--monitor', 'test1', 'test2', 'test3'], ['test1', 'test2', 'test3']),
    (['-m', ''], ['']),
    (['--monitor', ''], [''])
])

def test_monitor_args(mocker, monitor_args, monitor_result):
    mocker.patch('ouroboros.cli')
    cli.parser(monitor_args)
    assert cli.monitor == monitor_result

# Loglevel
@pytest.mark.parametrize('loglevel_args, loglevel_result', [
    (['-l', 'notset'], 'notset'),
    (['-l', 'info'], 'info'),
    (['-l', 'debug'], 'debug'),
    (['-l', 'warn'], 'warn'),
    (['-l', 'error'], 'error'),
    (['-l', 'critical'], 'critical'),
    (['--loglevel', 'notset'], 'notset'),
    (['--loglevel', 'info'], 'info'),
    (['--loglevel', 'debug'], 'debug'),
    (['--loglevel', 'warn'], 'warn'),
    (['--loglevel', 'error'], 'error'),
    (['--loglevel', 'critical'], 'critical')
])

def test_loglevel_args(mocker, loglevel_args, loglevel_result):
    mocker.patch('ouroboros.cli')
    cli.parser(loglevel_args)
    assert cli.level == loglevel_result

@pytest.mark.parametrize('runonce_args, runonce_result', [
    (['-r', ], True),
    (['--runonce', ], True)
])

def test_runonce_args(mocker, runonce_args, runonce_result):
    mocker.patch('ouroboros.cli')
    cli.parser(runonce_args)
    assert cli.run_once == runonce_result
