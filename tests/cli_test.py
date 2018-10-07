import pytest
import ouroboros.cli as cli
import sys
from mock import patch

def test_checkURI():
    assert cli.checkURI('tcp://0.0.0.0:1234')
    assert not cli.checkURI('tcp:/0.0.0.0')

@pytest.fixture
def create_parser(mocker):
    fake_args = [None, "--interval 0"]
    mocker.patch('sys.argv', fake_args)
    return cli.parser(sys.argv[1:])

def test_url_arg(create_parser):
    assert create_parser is not None
