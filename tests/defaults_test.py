import pytest
import ouroboros.defaults

def test_default_interval():
    assert ouroboros.defaults.INTERVAL == 300

def test_default_local_unix_socket():
    assert ouroboros.defaults.LOCAL_UNIX_SOCKET == 'unix://var/run/docker.sock'
