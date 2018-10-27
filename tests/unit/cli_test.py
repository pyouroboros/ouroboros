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
    # If none supplied, default to unix://
    (['-u', ''], defaults.LOCAL_UNIX_SOCKET),
    # Valid Regex
    (['-u', 'tcp://0.0.0.0:1234'], 'tcp://0.0.0.0:1234'),
])
def test_url_args(mocker, url_args, url_result):
    mocker.patch('ouroboros.cli')
    args = cli.parse(url_args)
    assert args.url == url_result

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
        cli.parse(['--interval', 'test'])
        assert pytest_wrapped_e.type == SystemExit


def test_interval_arg_valid_value(mocker):
    mocker.patch('ouroboros.cli')
    assert cli.parse(['--interval', 0])

# Monitor


@pytest.mark.parametrize('monitor_args, monitor_result', [
    (['-m', 'test1', 'test2', 'test3'], ['test1', 'test2', 'test3']),
    (['--monitor', 'test1', 'test2', 'test3'], ['test1', 'test2', 'test3']),
    (['-m', ''], ['']),
    (['--monitor', ''], [''])
])
def test_monitor_args(mocker, monitor_args, monitor_result):
    mocker.patch('ouroboros.cli')
    args = cli.parse(monitor_args)
    assert args.monitor == monitor_result

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
    args = cli.parse(loglevel_args)
    assert args.loglevel == loglevel_result


@pytest.mark.parametrize('loglevel_env_var, loglevel_env_var_result', [
    ({'LOGLEVEL': 'debug'}, 'debug'),
    ({'_LOGLEVEL': ''}, defaults.LOGLEVEL),
])
def test_loglevel_env_var(mocker, loglevel_env_var, loglevel_env_var_result):
    mocker.patch.dict('os.environ', loglevel_env_var)
    mocker.patch('ouroboros.cli')
    args = cli.parse([])
    assert args.loglevel == loglevel_env_var_result


@pytest.mark.parametrize('runonce_args, runonce_result', [
    (['-r', ], True),
    (['--runonce', ], True)
])
def test_runonce_args(mocker, runonce_args, runonce_result):
    mocker.patch('ouroboros.cli')
    args = cli.parse(runonce_args)
    assert args.run_once == runonce_result


@pytest.mark.parametrize('runonce_env_var, runonce_env_var_result', [
    ({'RUNONCE': 'true'}, 'true'),
    ({'_RUNONCE': ''}, defaults.RUNONCE),
])
def test_runonce_env_var(mocker, runonce_env_var, runonce_env_var_result):
    mocker.patch.dict('os.environ', runonce_env_var)
    mocker.patch('ouroboros.cli')
    args = cli.parse([])
    assert args.run_once == runonce_env_var_result


@pytest.mark.parametrize('cleanup_args, cleanup_result', [
    (['-c', ], True),
    (['--cleanup', ], True)
])
def test_cleanup_args(mocker, cleanup_args, cleanup_result):
    mocker.patch('ouroboros.cli')
    args = cli.parse(cleanup_args)
    assert args.cleanup == cleanup_result


@pytest.mark.parametrize('cleanup_env_var, cleanup_env_var_result', [
    ({'CLEANUP': 'true'}, 'true'),
    ({'_CLEANUP': ''}, defaults.CLEANUP),
])
def test_cleanup_env_var(mocker, cleanup_env_var, cleanup_env_var_result):
    mocker.patch.dict('os.environ', cleanup_env_var)
    mocker.patch('ouroboros.cli')
    args = cli.parse([])
    assert args.cleanup == cleanup_env_var_result
