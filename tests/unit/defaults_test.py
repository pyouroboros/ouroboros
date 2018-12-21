import pytest
import ouroboros.defaults as defaults

@pytest.mark.parametrize('default, result', [
    (defaults.INTERVAL, 300),
    (defaults.LOCAL_UNIX_SOCKET, 'unix://var/run/docker.sock'),
    (defaults.MONITOR, []),
    (defaults.IGNORE, []),
    (defaults.LOGLEVEL, 'info'),
    (defaults.RUNONCE, False),
    (defaults.CLEANUP, False),
    (defaults.METRICS_ADDR, '0.0.0.0'),
    (defaults.METRICS_PORT, 8000),
    (defaults.WEBHOOK_URLS, [])
])
def test_defaults(default, result):
    assert default == result
