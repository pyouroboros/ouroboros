import pytest
import ouroboros.cli as cli

def test_checkURI():
    assert cli.checkURI('tcp://0.0.0.0:1234') == True