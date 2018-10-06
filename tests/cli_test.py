import pytest
import ouroboros.cli as cli
import sys

def test_checkURI():
    assert cli.checkURI('tcp://0.0.0.0:1234')
    assert not cli.checkURI('tcp:/0.0.0.0')

def test_url_arg(mocker):
    fake_args = [None, "--url 0"]
    mocker.patch('sys.argv', fake_args)
    assert sys.argv[1] == '--url 0'