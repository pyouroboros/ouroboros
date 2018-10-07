import pytest
import ouroboros.cli as cli

def test_checkURI():
    assert cli.checkURI('tcp://0.0.0.0:1234')
    assert not cli.checkURI('tcp:/0.0.0.0')

@pytest.fixture
def create_parser(mocker):
    mocker.patch('sys.argv', '--interval 0')
    return cli.parser()

def test_url_arg(create_parser):
    assert create_parser == ' '
