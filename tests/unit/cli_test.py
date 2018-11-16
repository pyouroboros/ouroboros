from os import environ
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
def get_int_env_var(mocker, interval_env, interval_env_result):
    mocker.patch.dict('os.environ', interval_env)
    assert cli.get_int_env_var(env_var=environ.get('INTERVAL')) == interval_env_result


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


# Ignore
@pytest.mark.parametrize('ignore_args, ignore_result', [
    (['-n', 'test1', 'test2', 'test3'], ['test1', 'test2', 'test3']),
    (['--ignore', 'test1', 'test2', 'test3'], ['test1', 'test2', 'test3']),
    (['-n', ''], ['']),
    (['--ignore', ''], [''])
])
def test_ignore_args(mocker, ignore_args, ignore_result):
    mocker.patch('ouroboros.cli')
    args = cli.parse(ignore_args)
    assert args.ignore == ignore_result


# Log level
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


# Run once
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


# Cleanup
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


# Keeptag
@pytest.mark.parametrize('keeptag_args, keeptag_result', [
    (['-k', ], True),
    (['--keep-tag', ], True)
])
def test_keeptag_args(mocker, keeptag_args, keeptag_result):
    mocker.patch('ouroboros.cli')
    args = cli.parse(keeptag_args)
    assert args.keep_tag == keeptag_result


@pytest.mark.parametrize('keeptag_env_var, keeptag_env_var_result', [
    ({'KEEPTAG': 'true'}, 'true'),
    ({'_KEEPTAG': ''}, defaults.KEEPTAG),
])
def test_keeptag_env_var(mocker, keeptag_env_var, keeptag_env_var_result):
    mocker.patch.dict('os.environ', keeptag_env_var)
    mocker.patch('ouroboros.cli')
    args = cli.parse([])
    assert args.keep_tag == keeptag_env_var_result


# METRICS_ADDR
@pytest.mark.parametrize('metrics_addr_args, metrics_addr_result', [
    (['--metrics-addr', '0.0.0.1'], '0.0.0.1')
])
def test_metrics_addr_args(mocker, metrics_addr_args, metrics_addr_result):
    mocker.patch('ouroboros.cli')
    args = cli.parse(metrics_addr_args)
    assert args.metrics_addr == metrics_addr_result


@pytest.mark.parametrize('metrics_addr_env_var, metrics_addr_env_var_result', [
    ({'METRICS_ADDR': '0.0.0.1'}, '0.0.0.1'),
])
def test_metrics_addr_env_var(mocker, metrics_addr_env_var, metrics_addr_env_var_result):
    mocker.patch.dict('os.environ', metrics_addr_env_var)
    mocker.patch('ouroboros.cli')
    args = cli.parse([])
    assert args.metrics_addr == metrics_addr_env_var_result


# METRICS_PORT
@pytest.mark.parametrize('metrics_port_args, metrics_port_result', [
    (['--metrics-port', '8001'], 8001)
])
def test_metrics_port_args(mocker, metrics_port_args, metrics_port_result):
    mocker.patch('ouroboros.cli')
    args = cli.parse(metrics_port_args)
    assert args.metrics_port == metrics_port_result


@pytest.mark.parametrize('metrics_port_env_var, metrics_port_env_varresult', [
    ({'METRICS_PORT': 'test'}, False),
    ({'METRICS_PORT': '8001'}, 8001),
])
def get_metrics_port_int_env_var(mocker, metrics_port_env_var, metrics_port_env_var_result):
    mocker.patch.dict('os.environ', metrics_port_env_var)
    assert cli.get_int_env_var(env_var=environ.get('METRICS_PORT')) == metrics_port_env_var_result


def test_metrics_port_arg_invalid_value(mocker):
    mocker.patch('ouroboros.cli')
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        cli.parse(['--metrics-port', 'test'])
        assert pytest_wrapped_e.type == SystemExit
