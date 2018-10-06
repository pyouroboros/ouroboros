import pytest
import ouroboros.defaults as defaults

def test_default_interval():
    assert defaults.INTERVAL == 300

def test_default_local_unix_socket():
    assert defaults.LOCAL_UNIX_SOCKET == 'unix://var/run/docker.sock'
