import imp
import pytest
import ouroboros.cli as cli

def test_main(mocker):
    mocker.patch('sys.argv', [''])
    mocker.patch.dict('os.environ', {'INTERVAL': '6', 'LOGLEVEL': 'debug', 'RUNONCE': '', 'CLEANUP': ''})
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        assert imp.load_source('__main__', 'ouroboros/main.py') == SystemExit
